#!/bin/bash

# GITAM Login Generator - Production Start Script
# This script starts the application using Gunicorn (production server)

echo "=================================="
echo "Starting GITAM Login Generator"
echo "Production Mode with Gunicorn"
echo "=================================="
echo ""

# Set environment to production
export FLASK_ENV=production

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create .env file with required variables."
    exit 1
fi

# Load environment variables from .env
export $(cat .env | grep -v '^#' | xargs)

# Check required environment variables
if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_ANON_KEY" ]; then
    echo "❌ Error: Required environment variables not set!"
    echo "Please check SUPABASE_URL and SUPABASE_ANON_KEY in .env"
    exit 1
fi

echo "✓ Environment variables loaded"
echo "✓ Starting Gunicorn server..."
echo ""

# Start Gunicorn with production settings
gunicorn app:app \
    --bind 0.0.0.0:${PORT:-5001} \
    --workers 4 \
    --worker-class sync \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info

echo ""
echo "Server stopped."
