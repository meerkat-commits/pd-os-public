#!/usr/bin/env bash
# Scrubbed PD-OS export safe for public GitHub (meerkat-commits).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DEST="${1:-$REPO_ROOT/.github-publish}"

"$SCRIPT_DIR/export-pd-os-shareable.sh" "$DEST"

echo "Applying public GitHub redactions…"

# Internal metrics (Mozilla Looker DAU, etc.)
rm -rf "$DEST/data/metrics"

# Calibration + org-shift docs (ratings, named reports, Raja distribution)
rm -rf "$DEST/data/projects/2026-06-performance-review-calibration"
rm -rf "$DEST/data/projects/2026-07-ai-fluency-framework"

# Manager-only velocity drafts
rm -f "$DEST/data/projects/2026-06-ai-velocity-mandate/drafts/2026-06__raja-executive-summary.md"
rm -f "$DEST/data/projects/2026-06-ai-velocity-mandate/drafts/2026-06__team-facing-summary.md"

# Full decision registry with colleague POC names
rm -f "$DEST/data/projects/2026-02-project-nova/drafts/nova-decision-registry-rows.md"
rm -f "$DEST/data/projects/2026-02-project-nova/decisions.md"

# Internal mobile DAU investigation (show on request only)
rm -rf "$DEST/data/projects/2026-03-firefox-mobile-dau/research"
rm -f "$DEST/data/projects/2026-03-firefox-mobile-dau/brief.md"
rm -f "$DEST/scripts/ingest_granola_last_week.py"

# Replace colleague email map with examples
if [[ -f "$DEST/pd_os/granola_sync.py" ]]; then
  perl -i -0pe 's/EMAIL_DISPLAY: dict\[str, str\] = \{.*?\}/EMAIL_DISPLAY: dict[str, str] = {\n    "design.lead@example.com": "Design Lead",\n    "pm.partner@example.com": "PM Partner",\n}/s' \
    "$DEST/pd_os/granola_sync.py"
fi

# Redact named-manager references in operating rules
if [[ -f "$DEST/data/projects/2026-06-ai-velocity-mandate/drafts/2026-06__velocity-operating-rules.md" ]]; then
  perl -i -pe '
    s/Raja aligned on timing/Leadership aligned on timing/g;
    s/Raja rounded-corners model/rounded-corners fast-signal model/g;
  ' "$DEST/data/projects/2026-06-ai-velocity-mandate/drafts/2026-06__velocity-operating-rules.md"
fi

# Public-safe velocity brief (no manager doc link)
cat > "$DEST/data/projects/2026-06-ai-velocity-mandate/brief.shareable.md" <<'EOF'
# AI velocity mandate — shareable brief

**Public version** — no team audit tiers or internal partner context.

## Problem

Leadership needs confidence that Mobile & AI UX is moving faster with AI — more shipped decisions and user-visible fixes, not more hours — without design becoming QC for partner-built mocks.

## Goals

1. Monthly **proof** of shipped work, **decision quality** (not just speed), and throughput trend
2. Spread patterns that already work (Nova punch QA, visual papercuts, fast tactical research)
3. Instrument locally (Jira via Co-work); no new team-facing program

## Three bets

**Now:** QA and papercuts first. **Stretch:** code-native prototypes where the team is already shipping in the Firefox tree.

| Bet | Priority | Impact |
|-----|----------|--------|
| **QA & close the loop** | **Now** | Punch QA on Nova + **one backlog** for visual gaps (blocker / fix before exposure / accept & track). Papercuts post-Nightly. |
| **Faster calls** | Ongoing | Tactical vs strategic threshold — fast signal for reversible <48h calls; deep qual for big bets. Proof = signal **changed** a decision. |
| **Code, not slides** | **Stretch** | Eng-ready prototypes in the Firefox tree when it unblocks Eng — linked in sprint/ticket; not the default bar for everyone yet |

Operating detail: [`drafts/2026-06__velocity-operating-rules.md`](drafts/2026-06__velocity-operating-rules.md)

## Success (H2)

More **user-visible fixes** (QA closure, papercuts) and shipped low-risk surface area vs a one-month baseline — measured with proofs, not process overhead.

## Non-goals

- Headcount reduction framing
- Token-cost theater
- Paper-cut pilot before Nova in Nightly
- New standing meetings or surveys beyond existing AI training work
EOF

cat > "$DEST/data/projects/2026-06-ai-velocity-mandate/README.md" <<'EOF'
# AI velocity mandate — public example

**Owner:** Brooke Katalinich · **Example initiative** in PD-OS

Shareable operating model for design velocity with AI: proof bars, QA closure, fast tactical research, and code-native prototypes as stretch.

| Doc | Purpose |
|-----|---------|
| [`brief.shareable.md`](brief.shareable.md) | Public-safe problem, goals, three bets |
| [`drafts/2026-06__velocity-operating-rules.md`](drafts/2026-06__velocity-operating-rules.md) | Operating rules and proof bars |
| [`SHARE.md`](SHARE.md) | What's included vs excluded in public exports |

**Related:** [AI Native Knowledge Hub](https://github.com/FirefoxUX/ai-native-knowledge-hub)
EOF

cat > "$DEST/data/projects/2026-06-ai-velocity-mandate/SHARE.md" <<'EOF'
# AI velocity mandate — public sharing notes

This folder is a **redacted example** of how PD-OS stores an initiative workspace.

## Included (public)

- `brief.shareable.md` — problem, goals, three bets
- `drafts/2026-06__velocity-operating-rules.md` — proof bars and operating rules
- `jira.example.json` — config shape only (no real board IDs)

## Excluded (stays local)

- `brief.md`, `decisions.md`, `jira.json`, `metrics/`
- Manager 1:1 drafts, team audit, survey drafts
- `data/people/`, digests, calibration

Regenerate: `./setup/bin/export-public-github.sh`
EOF

# Replace old private repo URLs (careful with markdown link syntax)
find "$DEST" -type f \( -name '*.md' -o -name '*.html' -o -name '*.sh' \) -print0 \
  | xargs -0 perl -i -pe '
    s|https://github.com/meerkat-commits/pd-os)\]"]*|https://github.com/meerkat-commits/pd-os|g;
    s|https://github.com/meerkat-commits/pd-os)\]"]*|https://github.com/meerkat-commits/pd-os|g;
  '

# Generic stakeholder example in setup docs
perl -i -pe 's/"Raja Jacob"/"Example Stakeholder"/g' "$DEST/setup/README.md" 2>/dev/null || true
perl -i -pe 's/"Raja Jacob"/"Example Stakeholder"/g' "$DEST/pd_os/cli.py" 2>/dev/null || true

cat > "$DEST/README.md" <<'EOF'
# PD-OS — Brooke Katalinich

Public snapshot of a **Product Design Operating System**.

## What's here

| Path | Contents |
|------|----------|
| [`context-library/`](context-library/) | Stable product and process context |
| [`data/projects/`](data/projects/) | Example initiatives (Nova, velocity mandate) |
| [`pd_os/`](pd_os/) | Python CLI — digests, critique prep, dashboard |
| [`setup/`](setup/) | Agents, launchd templates, export scripts |

## Quick start (PD-OS)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 -m pd_os.cli dashboard --open
```

## Public vs private

This repo is a **redacted export**. Excluded: `data/people/`, meeting transcripts, calibration, internal metrics, manager 1:1 docs, full decision registries with colleague names.

Regenerate locally:

```bash
./setup/bin/export-public-github.sh
```

## Links

- AI Native Knowledge Hub: https://github.com/FirefoxUX/ai-native-knowledge-hub
- Maven (AI-Driven Design): https://maven.com/bkatalinich/ai-driven-design/preview/354376
- Substack: https://brookekatalinich.substack.com/
EOF

cat > "$DEST/SHARE.md" <<'EOF'
# Public GitHub export

This repository is generated by `setup/bin/export-public-github.sh` from a private PD-OS instance.

**Never committed from the private instance:** people memory, digests, inbox, calibration, Looker metrics, Jira exports, manager 1:1 drafts, full Nova decision registry with POC names.
EOF

# Final leakage scan (file content, not path references in docs)
WARN=0
LEAK_FILES=()
while IFS= read -r -d '' f; do
  case "$f" in
    *redaction-checklist*|*claude-workflow*|*export-public-github*|*export-pd-os-shareable*|*SHARE.md|*README.md|*CLAUDE.md|*how-i-work.md|*.gitignore)
      continue ;;
  esac
  if grep -q -E 'Mostly [Mm]eets|Greatly [Ee]xceeds|promotion not supported' "$f" 2>/dev/null; then
    LEAK_FILES+=("$f")
  fi
  if grep -q -E '@mozilla\.com' "$f" 2>/dev/null; then
    LEAK_FILES+=("$f")
  fi
  if grep -q 'Raja Jacob' "$f" 2>/dev/null; then
    LEAK_FILES+=("$f")
  fi
done < <(find "$DEST" -type f \( -name '*.md' -o -name '*.py' -o -name '*.json' -o -name '*.html' -o -name '*.sh' \) -print0)

if ((${#LEAK_FILES[@]})); then
  echo "WARNING: possible sensitive content in:"
  printf '  %s\n' "${LEAK_FILES[@]}" | sort -u
  WARN=1
fi
if [[ -d "$DEST/data/metrics" ]]; then
  echo "WARNING: data/metrics still present"
  WARN=1
fi

echo ""
echo "Public export ready: $DEST"
if [[ "$WARN" -eq 1 ]]; then
  echo "Review warnings before pushing to GitHub."
  exit 1
fi
echo "No obvious sensitive patterns detected."
