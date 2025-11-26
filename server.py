#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTTP Server for DOCX to Markdown Converter
Provides REST API for the Chrome extension
"""

import os
import sys
import json
import tempfile
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import cgi

# Add parent directory to path to import md_trans
sys.path.insert(0, str(Path(__file__).parent.parent / 'anylisppt'))

try:
    from md_trans import DocxToMarkdown
except ImportError:
    print("Error: Cannot import md_trans module")
    print("Please make sure md_trans.py is in the parent anylisppt directory")
    sys.exit(1)


class CORSHTTPRequestHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler with CORS support"""

    def _set_cors_headers(self):
        """Set CORS headers to allow cross-origin requests"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def _send_json_response(self, data, status=200):
        """Send JSON response"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self._set_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def do_OPTIONS(self):
        """Handle preflight OPTIONS request"""
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)

        if parsed_path.path == '/health':
            self._send_json_response({
                'status': 'ok',
                'message': 'Server is running'
            })
        else:
            self._send_json_response({
                'error': 'Not Found'
            }, status=404)

    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)

        if parsed_path.path == '/convert':
            self.handle_convert()
        else:
            self._send_json_response({
                'error': 'Not Found'
            }, status=404)

    def handle_convert(self):
        """Handle file conversion request"""
        try:
            # Parse multipart form data
            content_type = self.headers['Content-Type']
            if not content_type or not content_type.startswith('multipart/form-data'):
                self._send_json_response({
                    'success': False,
                    'error': 'Invalid content type'
                }, status=400)
                return

            # Parse form data
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    'REQUEST_METHOD': 'POST',
                    'CONTENT_TYPE': content_type,
                }
            )

            # Get file
            if 'file' not in form:
                self._send_json_response({
                    'success': False,
                    'error': 'No file provided'
                }, status=400)
                return

            file_item = form['file']
            if not file_item.file:
                self._send_json_response({
                    'success': False,
                    'error': 'Empty file'
                }, status=400)
                return

            # Get options
            extract_images = form.getvalue('extract_images', 'true').lower() == 'true'
            auto_convert = form.getvalue('auto_convert', 'false').lower() == 'true'
            output_path = form.getvalue('output_path', '')

            # Save uploaded file to temp location
            original_filename = file_item.filename
            # Extract just the filename (remove any path components from folder selection)
            filename_only = Path(original_filename).name

            temp_dir = tempfile.mkdtemp()
            temp_file = Path(temp_dir) / filename_only

            with open(temp_file, 'wb') as f:
                f.write(file_item.file.read())

            # Determine output path
            if output_path:
                output_file = Path(output_path) / Path(filename_only).with_suffix('.md').name
            else:
                # Use the original path structure if available, otherwise temp path
                if '/' in original_filename or '\\' in original_filename:
                    # Try to preserve the directory structure
                    output_file = Path(original_filename).with_suffix('.md')
                else:
                    output_file = temp_file.with_suffix('.md')

            # Ensure output directory exists
            output_file.parent.mkdir(parents=True, exist_ok=True)

            # Convert file
            converter = DocxToMarkdown(
                auto_convert_doc=auto_convert,
                extract_images=extract_images
            )

            markdown = converter.convert_file(temp_file, output_file)

            # Get image info
            image_count = len(converter.image_map) if converter.image_map else 0

            # Clean up temp file
            if temp_file.exists():
                temp_file.unlink()
            if temp_dir and Path(temp_dir).exists():
                import shutil
                shutil.rmtree(temp_dir, ignore_errors=True)

            # Send success response
            self._send_json_response({
                'success': True,
                'output_file': str(output_file),
                'image_count': image_count,
                'message': f'Successfully converted {filename_only}'
            })

        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            print(f"Error converting file: {error_detail}")
            self._send_json_response({
                'success': False,
                'error': str(e)
            }, status=500)

    def log_message(self, format, *args):
        """Custom log message format"""
        print(f"[{self.log_date_time_string()}] {format % args}")


def run_server(host='localhost', port=8765):
    """Run the HTTP server"""
    server_address = (host, port)
    httpd = HTTPServer(server_address, CORSHTTPRequestHandler)

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  DOCX to Markdown Converter Server                          ║
║  Server running at: http://{host}:{port:<4d}                      ║
║  Press Ctrl+C to stop                                        ║
╚══════════════════════════════════════════════════════════════╝
""")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
        httpd.shutdown()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='DOCX to Markdown Converter Server')
    parser.add_argument('--host', default='localhost', help='Server host (default: localhost)')
    parser.add_argument('--port', type=int, default=8765, help='Server port (default: 8765)')

    args = parser.parse_args()

    run_server(host=args.host, port=args.port)
