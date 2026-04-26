from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from backend.patterns import get_pattern, list_patterns, render_pattern


ROOT = Path(__file__).resolve().parents[1]
FRONTEND_DIR = ROOT / "frontend"
MAX_SIZE = 50
DEFAULT_SIZE = 5
DEFAULT_WIDTH = 5
DEFAULT_HEIGHT = 5


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

        try:
            pattern_id = _first(params, "pattern", "hill")
            spec = get_pattern(pattern_id)

            if spec is None:
                raise ValueError("Invalid pattern.")

            result = render_pattern(
                pattern_id=pattern_id,
                symbol=_first(params, "symbol", "*"),
                size=get_int(params, "size", DEFAULT_SIZE),
                width=get_int(params, "width", DEFAULT_WIDTH),
                height=get_int(params, "height", DEFAULT_HEIGHT),
            )
        except ValueError as error:
            self._send_json({"error": str(error)}, 400)
            return
        except Exception:
            self._send_json({"error": "Internal server error"}, 500)
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


def get_int(params: dict[str, list[str]], param: str, default: int) -> int:
    try:
        value = int(_first(params, param, str(default)))
    except ValueError as error:
        raise ValueError(f"{param} must be an integer") from error

    validate_range(value, param)
    return value


def validate_range(value: int, name: str) -> None:
    if not isinstance(value, int) or value < 1 or value > MAX_SIZE:
        raise ValueError(f"{name} must be between 1 and {MAX_SIZE}")


def main() -> None:
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    server = ThreadingHTTPServer((host, port), PatternPrinterHandler)
    print(f"Pattern Printer is running on {host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
