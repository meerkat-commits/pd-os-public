from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RepoPaths:
    root: Path

    @property
    def data(self) -> Path:
        return self.root / "data"

    @property
    def knowledge(self) -> Path:
        return self.data / "knowledge"

    @property
    def projects(self) -> Path:
        return self.data / "projects"

    @property
    def people(self) -> Path:
        return self.data / "people"

    @property
    def inbox_transcripts(self) -> Path:
        return self.data / "inbox" / "transcripts"


def repo_root_from_here() -> Path:
    # pd_os/paths.py -> pd-os/
    return Path(__file__).resolve().parents[1]


def ensure_base_folders(root: Path) -> RepoPaths:
    paths = RepoPaths(root=root)
    paths.knowledge.mkdir(parents=True, exist_ok=True)
    paths.projects.mkdir(parents=True, exist_ok=True)
    paths.people.mkdir(parents=True, exist_ok=True)
    paths.inbox_transcripts.mkdir(parents=True, exist_ok=True)
    return paths

