"""Local dev server with UTF-8 charset for .md and .html files."""
import http.server
import socketserver
import os
import sys

PORT = 8765
ROOT = r"C:\Kids\30_MiddleSchool\260426_MathTelling_Idea\50_units"

class UTF8Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        '.md': 'text/markdown; charset=utf-8',
        '.html': 'text/html; charset=utf-8',
        '.htm': 'text/html; charset=utf-8',
        '.js': 'application/javascript; charset=utf-8',
        '.css': 'text/css; charset=utf-8',
        '.json': 'application/json; charset=utf-8',
        '': 'application/octet-stream',
    }

    def end_headers(self):
        # No-cache so edits show immediately
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

os.chdir(ROOT)
with socketserver.TCPServer(("", PORT), UTF8Handler) as httpd:
    print(f"Serving {ROOT} at http://localhost:{PORT}")
    sys.stdout.flush()
    httpd.serve_forever()
