"""Local web dashboard for PD-OS artifacts and agents."""

from __future__ import annotations

import json
import re
import webbrowser
from dataclasses import dataclass
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from pd_os.agents_catalog import (
    agents_index,
    build_critique_prep_prompt,
    safe_readable_path,
    save_critique_draft,
)
from pd_os.paths import ensure_base_folders, repo_root_from_here

_STATIC_DIR = Path(__file__).resolve().parent / "static"


def _dashboard_html() -> bytes:
    path = _STATIC_DIR / "dashboard.html"
    return path.read_bytes()


@dataclass(frozen=True)
class Artifact:
    id: str
    title: str
    meta: str
    path: Path
    section: str
    mtime: float


def _friendly_title(path: Path) -> str:
    name = path.stem
    if re.match(r"^\d{4}-\d{2}-\d{2}$", name):
        return f"Daily digest · {name}"
    if name.startswith("commitments-"):
        return f"Commitments · {name.removeprefix('commitments-')}"
    if name.startswith("project-hygiene-"):
        return f"Project hygiene · {name.removeprefix('project-hygiene-')}"
    if "__to__" in name:
        start, end = name.split("__to__", 1)
        return f"Weekly rollup · {start} → {end}"
    if "__" in name:
        day, person = name.split("__", 1)
        return f"{person.replace('_', ' ')} · {day}"
    return name.replace("_", " ")


def _collect_artifacts(root: Path) -> list[Artifact]:
    paths = ensure_base_folders(root)
    items: list[Artifact] = []

    def add(section: str, glob: str, base: Path) -> None:
        if not base.exists():
            return
        for p in base.glob(glob):
            if not p.is_file() or p.suffix != ".md":
                continue
            rel = p.relative_to(root)
            stat = p.stat()
            items.append(
                Artifact(
                    id=str(rel).replace("\\", "/"),
                    title=_friendly_title(p),
                    meta=datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
                    path=p,
                    section=section,
                    mtime=stat.st_mtime,
                )
            )

    add("scratch", "*.md", paths.data / "digests")
    add("weekly", "*.md", paths.data / "rollups" / "weekly")
    add("stakeholder", "*.md", paths.data / "drafts" / "stakeholder")
    add("critique", "*.md", paths.data / "drafts" / "critique-prep")

    out: list[Artifact] = []
    for a in items:
        fname = a.path.name
        if fname.startswith("commitments-"):
            out.append(Artifact(a.id, a.title, a.meta, a.path, "commitments", a.mtime))
        elif fname.startswith("project-hygiene-"):
            out.append(Artifact(a.id, a.title, a.meta, a.path, "hygiene", a.mtime))
        elif "rollups/weekly" in a.id.replace("\\", "/"):
            out.append(a)
        elif "drafts/stakeholder" in a.id.replace("\\", "/"):
            out.append(a)
        elif "drafts/critique-prep" in a.id.replace("\\", "/"):
            out.append(a)
        else:
            out.append(Artifact(a.id, a.title, a.meta, a.path, "daily", a.mtime))
    return out


def build_file_index(root: Path) -> dict[str, Any]:
    artifacts = _collect_artifacts(root)
    sections_spec = [
        ("daily", "Daily digest"),
        ("commitments", "Commitments"),
        ("hygiene", "Project hygiene"),
        ("weekly", "Weekly rollups"),
        ("stakeholder", "Stakeholder drafts"),
        ("critique", "Critique prep drafts"),
    ]
    sections: list[dict[str, Any]] = []
    default_id: str | None = None

    for key, label in sections_spec:
        files = [a for a in artifacts if a.section == key]
        files.sort(key=lambda a: a.mtime, reverse=True)
        section_files = [{"id": a.id, "title": a.title, "meta": a.meta} for a in files]
        sections.append({"key": key, "label": label, "files": section_files})
        if key == "daily" and files and default_id is None:
            default_id = files[0].id

    return {"sections": sections, "default_id": default_id}


class DashboardHandler(BaseHTTPRequestHandler):
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

    def _safe_artifact_path(self, rel_id: str) -> Path | None:
        rel_id = rel_id.lstrip("/")
        candidate = (self.root / rel_id).resolve()
        try:
            candidate.relative_to(self.root.resolve())
        except ValueError:
            return None
        allowed_prefixes = (
            "data/digests/",
            "data/rollups/weekly/",
            "data/drafts/stakeholder/",
            "data/drafts/critique-prep/",
        )
        norm = str(candidate.relative_to(self.root.resolve())).replace("\\", "/")
        if not any(norm.startswith(p) for p in allowed_prefixes):
            return None
        if not candidate.is_file() or candidate.suffix != ".md":
            return None
        return candidate

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path in ("/", "/index.html"):
            self._send(200, _dashboard_html(), "text/html; charset=utf-8")
            return
        if parsed.path == "/api/files":
            self._json(build_file_index(self.root))
            return
        if parsed.path == "/api/agents":
            self._json(agents_index())
            return
        if parsed.path == "/api/changelog":
            path = safe_readable_path(self.root, "CHANGELOG.md")
            if path is None:
                self._json({"error": "not found"}, code=404)
                return
            self._json({"content": path.read_text(encoding="utf-8", errors="replace")})
            return
        if parsed.path == "/api/content":
            qs = parse_qs(parsed.query)
            rel_id = (qs.get("id") or [""])[0]
            path = self._safe_artifact_path(rel_id)
            if path is None:
                self._json({"error": "not found"}, code=404)
                return
            self._json({"id": rel_id, "content": path.read_text(encoding="utf-8", errors="replace")})
            return
        if parsed.path == "/api/agent":
            qs = parse_qs(parsed.query)
            rel_id = (qs.get("id") or [""])[0]
            path = safe_readable_path(self.root, rel_id)
            if path is None:
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


def serve_dashboard(*, host: str = "127.0.0.1", port: int = 8765, open_browser: bool = False) -> None:
    root = repo_root_from_here()
    handler = type("BoundDashboardHandler", (DashboardHandler,), {"root": root})
    server = ThreadingHTTPServer((host, port), handler)
    url = f"http://{host}:{port}/"
    print(f"PD-OS dashboard: {url}")
    print("  Artifacts · Agents · Changelog")
    print("Press Ctrl+C to stop.")
    if open_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        server.server_close()
