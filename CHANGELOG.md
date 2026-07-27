# Changelog — pd-os (PD-OS)

## [Unreleased]

### Fixed

- **Nova nightly screenshots — `new-tab` (05) and `smart-window` (07) no longer blank.** Marionette suppresses Activity Stream / `about:newtab` content for automation stability, so NTP-content shots now use a **hybrid no-marionette capture path** (`ShotSpec.requires_no_marionette`, `automation: "hybrid"` in `shots.json`). Three sub-fixes: (1) drop `-marionette` for flagged shots, (2) launch via direct binary instead of `open -na` (Launch Services was dropping `-no-remote`/`-profile` on some startups), (3) skip the `about:newtab → about:blank` URL deferral that was meant for the Marionette path. Bumped wait budget to 12s + 1.5s post-focus settle. See [`data/projects/2026-06-nova-nightly-screenshots/issues.md`](data/projects/2026-06-nova-nightly-screenshots/issues.md) ISSUE-001.
- **Offline-resilient Nightly version detection.** `fetch_nightly_version()` now reads `CFBundleShortVersionString` from the local `Firefox Nightly.app/Contents/Info.plist` first, falls back to product-details JSON, and finally to `"unknown"`. Captures no longer fail when VPN/DNS is unavailable.

### Added

- **Dashboard — Agents UI** (`python3 -m pd_os.cli dashboard --open`): browse team/manager/personal agents, **Critique prep form** (generates Cursor prompt + Slack skeleton), save drafts to `data/drafts/critique-prep/`, **Changelog** tab.
- **Critique slice** (`python3 -m pd_os.cli critique-dashboard --open`): standalone critique-only UI on port **8767** — form + principles/workflow docs. Export for team: `setup/bin/export-critique-slice.sh`.
- **Critique prep agent** for ICs: `setup/agents/critique-prep.md`, `context-library/process/critique-prep.md`, `.claude/skills/critique_prep.md`.
- **Heuristics review agent** for ICs: `setup/agents/heuristics-review.md`, `.claude/skills/heuristics_review.md` — routes to `design/heuristics-plugin/.cursor/skills/heuristics-review-bundle/`.

### Changed

- **Team skills moved to AI Native Knowledge Hub** — removed duplicated `.claude/skills/` routers and `sub-agents/`; `setup/agents/critique-prep.md` and `heuristics-review.md` now route to the hub. Dashboard Agents tab lists hub indexes + local PD-OS skills only.
- README: **Async design review (Mobile + AI)** section linking **[design-review-workflow](../../design/design-review-workflow/README.md)** and how initiative folders / templates align with **`#mobile_x_ai`** Slack cadence.
- **[`OPEN_ITEMS.md`](OPEN_ITEMS.md)** — checklist (venv, `data/`, ingest, templates/skills, review + Heuristics links); README intro links to it.

## [2026-04-19]

### Changed

- Lives under **`~/VibeCoding_BK/work/pd-os/`** (was briefly under `design/` during an intermediate layout). README quick-start `cd` path updated. See workspace [`CHANGELOG.md`](../../CHANGELOG.md).
