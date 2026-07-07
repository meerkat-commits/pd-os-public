"""Record nightly capture → FigJam placeholder sync jobs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pd_os.nightly_screenshots import DEFAULT_PROJECT_SLUG, project_dir


def figjam_config_path(root: Path, slug: str) -> Path:
    return project_dir(root, slug) / "figjam.json"


def load_figjam_config(root: Path, slug: str = DEFAULT_PROJECT_SLUG) -> dict[str, Any]:
    path = figjam_config_path(root, slug)
    if not path.exists():
        raise FileNotFoundError(f"Missing FigJam config: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_pending_sync(
    capture_dir: Path,
    *,
    root: Path,
    slug: str = DEFAULT_PROJECT_SLUG,
) -> Path:
    """Write a pending-sync manifest for MCP upload_assets (or manual follow-up)."""
    config = load_figjam_config(root, slug)
    manifest_path = capture_dir / "manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"Missing capture manifest: {manifest_path}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    placeholders: dict[str, str] = config.get("placeholders", {})
    uploads: list[dict[str, str]] = []

    for shot in manifest.get("shots", []):
        if shot.get("status") != "ok":
            continue
        shot_id = shot["id"]
        node_id = placeholders.get(shot_id)
        png = capture_dir / shot["filename"]
        if not node_id or not png.exists():
            continue
        uploads.append(
            {
                "shot_id": shot_id,
                "node_id": node_id,
                "png": str(png),
                "filename": shot["filename"],
            }
        )

    pending = {
        "file_key": config["file_key"],
        "file_url": config.get("file_url"),
        "capture_dir": str(capture_dir),
        "nightly_version": manifest.get("nightly_version"),
        "uploads": uploads,
    }
    out = project_dir(root, slug) / ".state" / "figjam-pending.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(pending, indent=2) + "\n", encoding="utf-8")
    return out
