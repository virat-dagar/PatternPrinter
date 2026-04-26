from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from backend.patterns import get_pattern, list_patterns, render_pattern


ROOT = Path(__file__).resolve().parents[1]
FRONTEND_DIR = ROOT / "frontend"


class PatternPrinterHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND_DIR), **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/patterns":
            self._send_json({"patterns": list_patterns()})
            return

        if parsed.path == "/api/render":
            self._handle_render(parsed.query)
            return

        if parsed.path == "/health":
            self._send_json({"status": "ok"})
            return

        if parsed.path == "/":
            self.path = "/index.html"

        return super().do_GET()

    def _handle_render(self, query: str) -> None:
        params = parse_qs(query)
        pattern_id = _first(params, "pattern", "hill")
        spec = get_pattern(pattern_id)

        if spec is None:
            self._send_json({"error": "Unknown pattern."}, 404)
            return

        try:
            result = render_pattern(
                pattern_id=pattern_id,
                symbol=_first(params, "symbol", "*"),
                size=_as_int(_first(params, "size", "6")),
                width=_as_int(_first(params, "width", "12")),
                height=_as_int(_first(params, "height", "6")),
            )
        except ValueError as error:
            self._send_json({"error": str(error)}, 400)
            return

        self._send_json({"pattern": spec.__dict__, "output": result})

    def _send_json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def _first(params: dict[str, list[str]], key: str, default: str) -> str:
    return params.get(key, [default])[0]


def _as_int(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        return 1


def main() -> None:
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    server = ThreadingHTTPServer((host, port), PatternPrinterHandler)
    print(f"Pattern Printer is running on {host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
