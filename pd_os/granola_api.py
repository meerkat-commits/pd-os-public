from __future__ import annotations

import json
import os
import re
import urllib.parse
import urllib.request
from urllib.error import HTTPError, URLError
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


class GranolaAuthError(RuntimeError):
    pass


def _api_key() -> str:
    key = os.environ.get("GRANOLA_API_KEY", "").strip()
    if not key:
        raise GranolaAuthError(
            "Missing GRANOLA_API_KEY environment variable. Create an API key in Granola and export GRANOLA_API_KEY before running."
        )
    # Granola Personal API keys are documented as starting with "grn_".
    # Validate early to avoid confusing HTTP 401s when the wrong token is used.
    if not re.match(r"^grn_[A-Za-z0-9_-]{16,}$", key):
        raise GranolaAuthError(
            "GRANOLA_API_KEY has an invalid format. Expected something like 'grn_...' (a Granola API key), "
            "not an OAuth/MCP token or placeholder value."
        )
    return key


def _request_json(url: str) -> Any:
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {_api_key()}")
    req.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            return json.loads(raw)
    except HTTPError as e:
        # Provide actionable guidance for common auth failures.
        if e.code in (401, 403):
            body = ""
            try:
                body = (e.read() or b"").decode("utf-8", errors="replace")
            except Exception:
                body = ""
            hint = ""
            if body:
                try:
                    j = json.loads(body)
                    hint = j.get("message") or j.get("error") or ""
                except Exception:
                    hint = body.strip()
            raise GranolaAuthError(
                "Granola API rejected GRANOLA_API_KEY (HTTP "
                f"{e.code}). Verify you exported the correct key and that the process running `pd_os` has access to it."
                + (f" API said: {hint}" if hint else "")
            ) from e
        raise
    except URLError as e:
        raise RuntimeError(f"Failed to reach Granola API: {e}") from e


def _iso(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass(frozen=True)
class GranolaNote:
    id: str
    title: str
    created_at: str | None
    start_time: str | None
    web_url: str | None
    summary_markdown: str | None
    attendees: list[dict[str, Any]] | None
    transcript: list[dict[str, Any]] | None


def list_notes(*, created_after: datetime, created_before: datetime | None = None) -> list[dict[str, Any]]:
    """
    Returns raw note items. Granola API is paginated; we follow cursors if present.
    """
    base = "https://public-api.granola.ai/v1/notes"
    params: dict[str, str] = {"created_after": _iso(created_after)}
    if created_before is not None:
        params["created_before"] = _iso(created_before)

    url = f"{base}?{urllib.parse.urlencode(params)}"
    out: list[dict[str, Any]] = []

    while True:
        data = _request_json(url)
        items = data.get("data") or data.get("notes") or []
        if not isinstance(items, list):
            break
        out.extend(items)

        next_url = data.get("next") or data.get("next_url")
        if not next_url:
            break
        url = next_url

    return out


def get_note(*, note_id: str, include_transcript: bool = True) -> GranolaNote:
    base = f"https://public-api.granola.ai/v1/notes/{note_id}"
    url = base
    if include_transcript:
        url = f"{base}?include=transcript"

    data = _request_json(url)
    return GranolaNote(
        id=data.get("id", note_id),
        title=data.get("title") or "(untitled)",
        created_at=data.get("created_at"),
        start_time=(data.get("calendar_event") or {}).get("start_time") if isinstance(data.get("calendar_event"), dict) else data.get("start_time"),
        web_url=data.get("web_url"),
        summary_markdown=data.get("summary_markdown"),
        attendees=data.get("attendees"),
        transcript=data.get("transcript"),
    )

