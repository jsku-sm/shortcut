"""Run the shortest-path web app with Python's built-in HTTP server."""

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


class AppHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.split("?", 1)[0] == "/":
            self.path = "/river_shortest_path.html"
        super().do_GET()

    def do_HEAD(self):
        if self.path.split("?", 1)[0] == "/":
            self.path = "/river_shortest_path.html"
        super().do_HEAD()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    handler = partial(AppHandler, directory=str(Path(__file__).resolve().parent))
    try:
        server = ThreadingHTTPServer((args.host, args.port), handler)
    except OSError as error:
        parser.exit(1, f"서버를 실행할 수 없습니다: {error}\n다른 포트를 사용해 보세요: python3 app.py --port 8001\n")
    with server:
        print(f"앱 주소: http://localhost:{args.port}/", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n서버를 종료합니다.")


if __name__ == "__main__":
    main()
