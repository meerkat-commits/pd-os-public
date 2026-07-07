"""Agent catalog and critique-prep prompt builder for the PD-OS dashboard."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Any

from pd_os.paths import ensure_base_folders, repo_root_from_here


@dataclass(frozen=True)
class AgentInfo:
    id: str
    title: str
    audience: str  # team | manager | personal
    summary: str
    has_form: bool = False
    form_type: str | None = None


AGENTS: tuple[AgentInfo, ...] = (
    AgentInfo(
        "setup/agents/critique-prep.md",
        "Critique prep",
        "team",
        "Hub + Mobile+AI workflow — decision-oriented async review packet",
        has_form=True,
        form_type="critique_prep",
    ),
    AgentInfo(
        "setup/agents/heuristics-review.md",
        "Heuristics review",
        "team",
        "Hub design skills — Nielsen / Acorn / craft pass (Figma plugin parity)",
    ),
    AgentInfo(
        "setup/agents/stakeholder-draft.md",
        "Stakeholder draft",
        "personal",
        "Stakeholder message context bundles",
    ),
    AgentInfo(
        "setup/agents/daily.md",
        "Daily review",
        "personal",
        "Review today's digest and commitments",
    ),
    AgentInfo(
        "setup/agents/weekly.md",
        "Weekly review",
        "personal",
        "Review weekly rollup themes",
    ),
)

HUB_ROOT = "../ai-native-knowledge-hub"
HUB_URL = "https://github.com/FirefoxUX/ai-native-knowledge-hub"

SKILLS: tuple[dict[str, str], ...] = (
    {
        "id": ".claude/skills/meeting_ingest.md",
        "title": "Meeting ingest",
        "summary": "Zoom transcript → data/people/ (pd_os.cli)",
    },
    {
        "id": ".claude/skills/smart_window_design.md",
        "title": "Smart Window design",
        "summary": "Firefox AI Window / motion — local manager scope",
    },
)

HUB_SKILLS: tuple[dict[str, str], ...] = (
    {
        "title": "Knowledge hub (start here)",
        "path": f"{HUB_ROOT}/AGENTS.md",
        "url": f"{HUB_URL}/blob/main/AGENTS.md",
        "summary": "Team skills, agents, templates — canonical source",
    },
    {
        "title": "Design skills",
        "path": f"{HUB_ROOT}/skills/design/SKILLS.md",
        "url": f"{HUB_URL}/blob/main/skills/design/SKILLS.md",
        "summary": "Critique, craft review, executive review",
    },
    {
        "title": "Content skills",
        "path": f"{HUB_ROOT}/skills/content/SKILLS.md",
        "url": f"{HUB_URL}/blob/main/skills/content/SKILLS.md",
        "summary": "Brand voice, strings, writing rules",
    },
    {
        "title": "Design system skills",
        "path": f"{HUB_ROOT}/skills/design-system/SKILLS.md",
        "url": f"{HUB_URL}/blob/main/skills/design-system/SKILLS.md",
        "summary": "Nova tokens, Supernova MCP, component specs",
    },
)

AUDIENCE_LABELS = {
    "team": "Team (ICs)",
    "manager": "Managers",
    "personal": "Personal",
}

READABLE_PREFIXES = (
    "setup/agents/",
    "context-library/process/",
    "sub-agents/",
    ".claude/skills/",
    "CHANGELOG.md",
    "templates/critique_notes.md",
)


def agents_index() -> dict[str, Any]:
    groups: dict[str, list[dict[str, Any]]] = {k: [] for k in AUDIENCE_LABELS}
    for agent in AGENTS:
        groups[agent.audience].append(asdict(agent))
    return {
        "groups": [{"audience": k, "label": AUDIENCE_LABELS[k], "agents": groups[k]} for k in AUDIENCE_LABELS],
        "skills": list(SKILLS),
        "hub_skills": list(HUB_SKILLS),
        "hub_url": HUB_URL,
    }


def safe_readable_path(root: Path, rel_id: str) -> Path | None:
    rel_id = rel_id.lstrip("/")
    if rel_id == "CHANGELOG.md":
        candidate = (root / rel_id).resolve()
    else:
        candidate = (root / rel_id).resolve()
    try:
        norm = str(candidate.relative_to(root.resolve())).replace("\\", "/")
    except ValueError:
        return None
    if norm != "CHANGELOG.md" and not any(norm.startswith(p) for p in READABLE_PREFIXES):
        return None
    if not candidate.is_file() or candidate.suffix != ".md":
        return None
    return candidate


def _slug(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:48] or "critique"


def build_critique_prep_prompt(payload: dict[str, Any]) -> dict[str, str]:
    figma = (payload.get("figma_url") or "").strip()
    frame = (payload.get("frame_name") or "").strip()
    jira = (payload.get("jira_key") or "").strip()
    phase = (payload.get("phase") or "Design").strip()
    decision_type = (payload.get("decision_type") or "Direction").strip()
    problem = (payload.get("problem_statement") or "").strip()
    if_no = (payload.get("if_no_alignment") or "").strip()
    constraints = (payload.get("constraints") or "").strip()
    owner = (payload.get("owner") or "").strip()
    by_when = (payload.get("by_when") or "").strip()
    initiative = (payload.get("initiative") or "").strip()
    exit_goal = (payload.get("exit_goal") or "").strip()
    nova = bool(payload.get("nova_in_scope"))

    decision_ask = problem or "TBD — state the primary decision or learning goal"
    slack_need = if_no or decision_ask

    slack_post = f"""Channel: #mobile_x_ai
[Mobile+AI · {phase}] {jira or "TBD title"}
Owner: {owner or "@…"}
Jira: {jira or "KEY-123"}
Figma: {figma or "<link>"} (frame: {frame or "<name>"})
Exit we're aiming for: {exit_goal or "<one line from phase list>"}
What we need: {slack_need}
By when: {by_when or "<date or sprint>"}
Thread = review.

**Critique questions**
1. …
2. …
3. …"""

    context_lines = [
        "Follow `../ai-native-knowledge-hub/AGENTS.md` → design skills, plus PD-OS Mobile+AI workflow below.",
        "Read `setup/agents/critique-prep.md` for the full hub + local context list.",
        "",
        "## Designer inputs",
        f"- **Figma:** {figma or 'TBD'} (frame: {frame or 'TBD'})",
        f"- **Jira:** {jira or 'TBD'}",
        f"- **Phase:** {phase}",
        f"- **Primary decision type:** {decision_type}",
        f"- **Problem / user job:** {problem or 'TBD'}",
        f"- **If reviewers say no:** {if_no or 'TBD'}",
        f"- **Constraints:** {constraints or 'TBD'}",
        f"- **Owner:** {owner or 'TBD'}",
        f"- **By when:** {by_when or 'TBD'}",
    ]
    if initiative:
        context_lines.append(f"- **Initiative folder:** `data/projects/{initiative}/` — read `brief.md` and `decisions.md` if present")
    if nova:
        context_lines.append("- **Nova in scope:** yes — check `context-library/design-md/nova-classic/DESIGN.md`")

    context_lines.extend(
        [
            "",
            "## Read first",
            "- `context-library/process/critique-prep.md`",
            "- `context-library/process/mobile_ai_design_review_workflow.md`",
            "- `context-library/product-and-design.md`",
            "",
            "Produce the full critique packet. Section 6 (Slack post) should be ready to paste with minimal edits.",
        ]
    )

    cursor_prompt = "\n".join(context_lines)

    return {
        "cursor_prompt": cursor_prompt,
        "slack_skeleton": slack_post,
        "agent_path": "setup/agents/critique-prep.md",
    }


def save_critique_draft(root: Path, payload: dict[str, Any], generated: dict[str, str]) -> Path:
    paths = ensure_base_folders(root)
    out_dir = paths.data / "drafts" / "critique-prep"
    out_dir.mkdir(parents=True, exist_ok=True)

    title = (payload.get("jira_key") or payload.get("problem_statement") or "critique")[:40]
    fname = f"{date.today().isoformat()}__{_slug(title)}.md"
    out_path = out_dir / fname

    lines = [
        "# Critique prep draft",
        "",
        f"**Saved:** {date.today().isoformat()}",
        "",
        "## Inputs",
        "",
        f"- Figma: {payload.get('figma_url', '')}",
        f"- Frame: {payload.get('frame_name', '')}",
        f"- Jira: {payload.get('jira_key', '')}",
        f"- Phase: {payload.get('phase', '')}",
        f"- Decision type: {payload.get('decision_type', '')}",
        f"- Problem: {payload.get('problem_statement', '')}",
        f"- If no alignment: {payload.get('if_no_alignment', '')}",
        f"- Constraints: {payload.get('constraints', '')}",
        f"- Owner: {payload.get('owner', '')}",
        f"- By when: {payload.get('by_when', '')}",
        "",
        "## Cursor prompt",
        "",
        "```text",
        generated["cursor_prompt"],
        "```",
        "",
        "## Slack skeleton",
        "",
        "```text",
        generated["slack_skeleton"],
        "```",
        "",
    ]
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path
