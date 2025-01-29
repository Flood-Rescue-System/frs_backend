#!/bin/bash
set -e  # Exit on error

# Install additional dependencies if needed
pip install -r requirements.txt

# Make script executable
chmod +x start.sh

# Set default port if not provided
export PORT="${PORT:-8000}"

# Start the application
uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --workers 1 