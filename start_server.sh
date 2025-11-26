#!/bin/bash

# Quick start script for DOCX to Markdown Converter Server

cd "$(dirname "$0")"

echo "=================================================="
echo "  DOCX to Markdown Converter Server"
echo "=================================================="
echo ""
echo "Starting server..."
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

# Check if python-docx is installed
python3 -c "import docx" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Warning: python-docx is not installed"
    echo "Installing python-docx..."
    pip3 install python-docx
    echo ""
fi

# Start the server
python3 server.py "$@"
