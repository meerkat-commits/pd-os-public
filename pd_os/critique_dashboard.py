"""Standalone critique-prep web UI — team slice of PD-OS."""

from __future__ import annotations

import json
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from pd_os.agents_catalog import (
    build_critique_prep_prompt,
    safe_readable_path,
    save_critique_draft,
)
from pd_os.paths import repo_root_from_here

_STATIC_DIR = Path(__file__).resolve().parent / "static"

CRITIQUE_DOCS: tuple[tuple[str, str], ...] = (
    ("context-library/process/critique-prep.md", "Principles"),
    ("context-library/process/mobile_ai_design_review_workflow.md", "Workflow"),
    ("setup/agents/critique-prep.md", "Agent prompt"),
    ("templates/critique_notes.md", "After critique"),
)


def _critique_html() -> bytes:
    return (_STATIC_DIR / "critique.html").read_bytes()


class CritiqueHandler(BaseHTTPRequestHandler):
    root: Path

    def log_message(self, format: str, *args: Any) -> None:
        return

    def _send(self, code: int, body: bytes, content_type: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, payload: dict[str, Any], code: int = 200) -> None:
        self._send(code, json.dumps(payload).encode("utf-8"), "application/json; charset=utf-8")

    def _read_json_body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", 0))
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        try:
            data = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            return {}
        return data if isinstance(data, dict) else {}

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path in ("/", "/index.html"):
            self._send(200, _critique_html(), "text/html; charset=utf-8")
            return
        if parsed.path == "/api/docs":
            self._json(
                {
                    "docs": [
                        {"id": doc_id, "title": title}
                        for doc_id, title in CRITIQUE_DOCS
                    ]
                }
            )
            return
        if parsed.path == "/api/doc":
            qs = parse_qs(parsed.query)
            rel_id = (qs.get("id") or [""])[0]
            path = safe_readable_path(self.root, rel_id)
            allowed = {doc_id for doc_id, _ in CRITIQUE_DOCS}
            if path is None or rel_id not in allowed:
                self._json({"error": "not found"}, code=404)
                return
            self._json({"id": rel_id, "content": path.read_text(encoding="utf-8", errors="replace")})
            return
        self._send(404, b"Not found", "text/plain; charset=utf-8")

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/critique-prep":
            payload = self._read_json_body()
            generated = build_critique_prep_prompt(payload)
            result: dict[str, Any] = dict(generated)
            if payload.get("save"):
                saved = save_critique_draft(self.root, payload, generated)
                result["saved_path"] = str(saved.relative_to(self.root)).replace("\\", "/")
            self._json(result)
            return
        self._send(404, b"Not found", "text/plain; charset=utf-8")


def serve_critique_dashboard(
    *,
    host: str = "127.0.0.1",
    port: int = 8767,
    open_browser: bool = False,
) -> None:
    root = repo_root_from_here()
    handler = type("BoundCritiqueHandler", (CritiqueHandler,), {"root": root})
    server = ThreadingHTTPServer((host, port), handler)
    url = f"http://{host}:{port}/"
    print(f"Critique prep UI: {url}")
    print("Press Ctrl+C to stop.")
    if open_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        server.server_close()
