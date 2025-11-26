#!/usr/bin/env python3
"""Test script to verify server functionality"""

import requests
import sys
from pathlib import Path

SERVER_URL = 'http://localhost:8765'

def test_health():
    """Test server health check"""
    print("Testing /health endpoint...")
    try:
        response = requests.get(f'{SERVER_URL}/health')
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"  Error: {e}")
        return False

def test_convert(file_path):
    """Test file conversion"""
    print(f"\nTesting /convert with file: {file_path}")

    if not Path(file_path).exists():
        print(f"  Error: File not found: {file_path}")
        return False

    try:
        with open(file_path, 'rb') as f:
            files = {'file': (Path(file_path).name, f, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')}
            data = {
                'extract_images': 'true',
                'auto_convert': 'false',
                'output_path': ''
            }

            response = requests.post(f'{SERVER_URL}/convert', files=files, data=data)
            print(f"  Status: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                print(f"  Success: {result.get('success')}")
                print(f"  Output: {result.get('output_file')}")
                print(f"  Images: {result.get('image_count')}")
                return result.get('success', False)
            else:
                print(f"  Error: {response.text}")
                return False

    except Exception as e:
        print(f"  Exception: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("  DOCX to Markdown Converter - Server Test")
    print("=" * 60)

    # Test health
    if not test_health():
        print("\n❌ Server is not running!")
        print("   Please start the server first: ./start_server.sh")
        sys.exit(1)

    print("\n✓ Server is running")

    # Test conversion if file is provided
    if len(sys.argv) > 1:
        test_file = sys.argv[1]
        if test_convert(test_file):
            print("\n✓ Conversion test passed")
        else:
            print("\n❌ Conversion test failed")
    else:
        print("\nℹ️  To test conversion, run:")
        print(f"   python3 {sys.argv[0]} /path/to/your/file.docx")

    print("\n" + "=" * 60)
