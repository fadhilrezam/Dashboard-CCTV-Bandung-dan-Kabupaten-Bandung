#!/usr/bin/env python3
"""Local CCTV dashboard + same-origin HLS proxy. Python standard library only."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, urljoin, quote
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from pathlib import Path
import re, os, mimetypes

ROOT = Path(__file__).resolve().parent
ALLOWED = {
    'pelindung.bandung.go.id',
    'cctv.bandungkab.go.id',
}
PORT = 8765

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/':
            self.send_response(302); self.send_header('Location', '/dashboard_cctv_bandung.html'); self.end_headers(); return
        if parsed.path != '/proxy':
            if parsed.path == '/dashboard_cctv_bandung.html':
                return super().do_GET()
            self.send_error(404, 'Not found'); return
        qs = parse_qs(parsed.query)
        target = qs.get('url', [''])[0]
        u = urlparse(target)
        if u.scheme != 'https' or u.hostname not in ALLOWED:
            self.send_error(403, 'Upstream host is not allowed')
            return
        origin = 'https://' + u.hostname
        headers = {
            'User-Agent': 'Mozilla/5.0 CCTV-Dashboard/1.0',
            'Origin': origin,
            'Referer': origin + '/',
            'Accept': '*/*',
        }
        try:
            req = Request(target, headers=headers)
            with urlopen(req, timeout=20) as resp:
                body = resp.read()
                ctype = resp.headers.get('Content-Type', 'application/octet-stream')
                final_url = resp.geturl()
            is_playlist = ('.m3u8' in u.path.lower() or 'mpegurl' in ctype.lower())
            if is_playlist:
                text = body.decode('utf-8', errors='replace')
                def proxify(ref):
                    absolute = urljoin(final_url, ref.strip())
                    return '/proxy?url=' + quote(absolute, safe='')
                out=[]
                for line in text.splitlines():
                    stripped=line.strip()
                    if not stripped:
                        out.append(line)
                    elif stripped.startswith('#'):
                        # Rewrite URI="..." attributes used by I-frame/media/key tags.
                        line=re.sub(r'URI="([^"]+)"', lambda m:'URI="'+proxify(m.group(1))+'"', line)
                        out.append(line)
                    else:
                        out.append(proxify(stripped))
                body=('\n'.join(out)+'\n').encode('utf-8')
                ctype='application/vnd.apple.mpegurl'
            self.send_response(200)
            self.send_header('Content-Type', ctype)
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(body)
        except HTTPError as e:
            self.send_error(e.code, 'Upstream CCTV server rejected the request')
        except (URLError, TimeoutError, OSError) as e:
            self.send_error(502, 'Could not reach upstream CCTV server: ' + str(e))

    def log_message(self, fmt, *args):
        # Keep console output concise; show proxy errors only.
        if self.path.startswith('/proxy') and args and str(args[1]) not in ('200',):
            super().log_message(fmt, *args)

if __name__ == '__main__':
    print('Dashboard CCTV berjalan di http://127.0.0.1:%d/dashboard_cctv_bandung.html' % PORT)
    print('Jangan tutup jendela ini selama dashboard digunakan.')
    ThreadingHTTPServer(('127.0.0.1', PORT), Handler).serve_forever()
