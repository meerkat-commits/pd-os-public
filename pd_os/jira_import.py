"""Import Jira board exports from Claude Co-work (no API token required)."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pd_os.jira_sync import (
    _render_snapshot_markdown,
    _summarize_board,
    _write_snapshot_files,
    load_config,
    project_slug_dir,
)


class JiraImportError(RuntimeError):
    pass


def _normalize_issue(row: dict[str, Any]) -> dict[str, Any]:
    assignee = row.get("assignee")
    return {
        "key": row.get("key"),
        "fields": {
            "summary": row.get("summary"),
            "status": {"name": row.get("status") or "Unknown"},
            "assignee": {"displayName": assignee} if assignee else None,
            "updated": row.get("updated"),
            "resolutiondate": row.get("resolutiondate"),
        },
    }


def _parse_markdown_tables(text: str) -> list[dict[str, Any]]:
    """Best-effort parse of markdown issue tables from Co-work output."""
    boards: list[dict[str, Any]] = []
    current_board: dict[str, Any] | None = None
    headers: list[str] = []

    for line in text.splitlines():
        heading = re.match(r"^##\s+(.+)$", line.strip())
        if heading:
            if current_board and current_board.get("issues"):
                boards.append(current_board)
            current_board = {
                "board_name": heading.group(1).strip(),
                "issues": [],
            }
            headers = []
            continue

        if not line.strip().startswith("|"):
            continue

        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells:
            continue
        if all(re.match(r"^[-:]+$", c) for c in cells):
            continue
        if not headers:
            headers = [h.lower().replace(" ", "_") for h in cells]
            continue
        if not current_board:
            current_board = {"board_name": "Imported board", "issues": []}

        row = dict(zip(headers, cells))
        key = row.get("key") or row.get("issue") or row.get("ticket")
        if not key:
            continue
        current_board["issues"].append(
            {
                "key": key,
                "summary": row.get("summary") or row.get("title") or "",
                "status": row.get("status") or "?",
                "assignee": row.get("assignee") or row.get("owner") or "Unassigned",
                "updated": row.get("updated"),
                "resolutiondate": row.get("resolutiondate") or row.get("resolved"),
            }
        )

    if current_board and current_board.get("issues"):
        boards.append(current_board)

    return boards


def _load_export(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        data = json.loads(text)
        if not isinstance(data, dict):
            raise JiraImportError("JSON root must be an object")
        return data

    # Markdown or .md — try JSON fence first, else tables
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fence:
        return json.loads(fence.group(1))

    boards = _parse_markdown_tables(text)
    if boards:
        return {"source": "claude-cowork", "boards": boards}

    raise JiraImportError(
        f"Could not parse {path.name}. Use JSON (see metrics/inbox/cowork-export.template.json) "
        "or markdown tables with columns: Key | Status | Assignee | Summary"
    )


def _match_board_config(export_board: dict[str, Any], config_boards: list) -> Any:
    bid = export_board.get("board_id")
    name = (export_board.get("board_name") or export_board.get("name") or "").lower()
    pkey = (export_board.get("project_key") or "").upper()

    for b in config_boards:
        if bid is not None and b.id == bid:
            return b
        if pkey and b.project_key.upper() == pkey:
            return b
        if name and b.name.lower() in name or name in b.name.lower():
            return b
    return None


def import_cowork_export(
    path: Path,
    *,
    project_slug: str,
    archive: bool = True,
) -> dict[str, Any]:
    """Ingest a Co-work Jira export and write metrics/latest.*"""
    path = path.expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(path)

    raw = _load_export(path)
    config = load_config(project_slug)
    window_days = int(raw.get("window_days") or config.velocity_window_days)

    export_boards = raw.get("boards") or []
    if not export_boards:
        raise JiraImportError("Export has no boards[]")

    board_summaries: list[dict[str, Any]] = []
    for eb in export_boards:
        cfg = _match_board_config(eb, config.boards)
        issues_raw = eb.get("issues") or []
        issues = [_normalize_issue(i) for i in issues_raw]

        board_meta = type(
            "B",
            (),
            {
                "id": eb.get("board_id") or (cfg.id if cfg else None),
                "name": eb.get("board_name") or eb.get("name") or (cfg.name if cfg else "Board"),
                "pillar": eb.get("pillar") or (cfg.pillar if cfg else ""),
                "manager": eb.get("manager") or (cfg.manager if cfg else ""),
                "project_key": eb.get("project_key") or (cfg.project_key if cfg else ""),
            },
        )()

        board_summaries.append(
            _summarize_board(
                board_meta,
                issues,
                status_groups=config.status_groups,
                window_days=window_days,
            )
        )

    total_completed = sum(b["completed_in_window"] for b in board_summaries)
    total_active = sum(
        b["status_buckets"].get("in_design", 0)
        + b["status_buckets"].get("ready_for_eng", 0)
        + b["status_buckets"].get("in_progress_eng", 0)
        for b in board_summaries
    )

    snapshot = {
        "project_slug": project_slug,
        "synced_at": raw.get("synced_at") or datetime.now(timezone.utc).isoformat(),
        "source": raw.get("source") or "claude-cowork",
        "import_file": str(path),
        "site": config.site,
        "window_days": window_days,
        "boards": board_summaries,
        "totals": {
            "issues_on_boards": sum(b["issue_count"] for b in board_summaries),
            "completed_in_window": total_completed,
            "active_pipeline": total_active,
            "weekly_velocity_estimate": round(total_completed / max(window_days / 7, 1), 1),
        },
    }

    json_path, md_path = _write_snapshot_files(project_slug, snapshot)

    if archive:
        inbox = project_slug_dir(project_slug) / "metrics" / "inbox"
        inbox.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        archive_path = inbox / f"cowork-{stamp}{path.suffix}"
        archive_path.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")

    snapshot["_written"] = {"json": str(json_path), "markdown": str(md_path)}
    return snapshot
