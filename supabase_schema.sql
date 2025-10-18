-- Supabase Schema for GITAM Login Records
-- Run this in your Supabase SQL Editor

-- Create the login_records table
CREATE TABLE IF NOT EXISTS login_records (
    id BIGSERIAL PRIMARY KEY,
    roll_number VARCHAR(50) NOT NULL,
    encrypted_password TEXT NOT NULL, -- Stores plain password (column name kept for compatibility)
    uid_url TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    ip_address VARCHAR(45), -- Store IP for security monitoring
    user_agent TEXT, -- Store user agent for security
    last_accessed TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- Create index on roll_number for faster lookups
CREATE INDEX IF NOT EXISTS idx_roll_number ON login_records(roll_number);

-- Create index on created_at for sorting
CREATE INDEX IF NOT EXISTS idx_created_at ON login_records(created_at DESC);

-- Enable Row Level Security (RLS)
ALTER TABLE login_records ENABLE ROW LEVEL SECURITY;

-- Create policy to allow INSERT operations (for logging logins)
CREATE POLICY "Allow insert for all users" ON login_records
    FOR INSERT
    WITH CHECK (true);

-- Create policy to allow SELECT only for authenticated users (optional - adjust as needed)
-- Comment this out if you want public read access
CREATE POLICY "Allow select for all users" ON login_records
    FOR SELECT
    USING (true);

-- Add comment to table
COMMENT ON TABLE login_records IS 'Stores GITAM login records with plain passwords';
COMMENT ON COLUMN login_records.encrypted_password IS 'Password stored in plain text (column name kept for compatibility)';
COMMENT ON COLUMN login_records.uid_url IS 'Full URL with encrypted ID parameter';
