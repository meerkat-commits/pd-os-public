# Nova Nightly screenshots — brief

**Date:** 2026-06 · **Owner:** Brooke Katalinich

## Purpose

Daily punch-QA captures from **Firefox Nightly** with `browser.nova.enabled` on. Feeds the velocity mandate visual-gap backlog (Lever 1).

**QA depth:** `qa-test-cases.md` — foxfooding-granularity test cases mapped to shots 01–17.

**Open issues:** `issues.md` — automation blockers and status (ISSUE-001 NTP blank under Marionette is the main gap).

## What we automate (and what we don’t)

Marionette is good at **URLs + prefs**. It is poor at **privileged chrome state** (themes, collapsed tab groups, session restore). We split shots into three tiers in `shots.json` (`automation` field).

| Tier | Default daily run? | Shots | Why |
|------|-------------------|-------|-----|
| **automated** | Yes | 01–03, 06, 08–12, 14–15, 17 | Prefs, URL, or stable chrome commands |
| **automated (blocked)** | Yes, but warns | 05 new-tab, 07 smart-window | Marionette suppresses Activity Stream — see ISSUE-001 |
| **best_effort** | No (`--include-best-effort`) | 04 tab-grouping | Chrome script may work; often wrong |
| **manual** | No | 13 chrome-dark, 16 tab-grouping-collapsed | Theme + collapse selection don’t stick in automation |

**Manual steps:** `manual-checklist.md` (~2–3 min). Drop PNGs into the same `captures/YYYY-MM-DD__<version>/` folder as automated shots.

**Manifest honesty:** `status` is `ok`, `warning` (setup checks failed), `error`, or `skipped`. Warnings are listed per shot — a PNG is not treated as a clean pass when setup failed.

### Why automation blocked on some shots

- **Chrome ≠ content** — Marionette targets pages; tab groups, themes, and sidebar state live in privileged browser UI.
- **Profile bleed** — `sessionstore`, `extensions.json`, and theme state persist across shots unless cleared each run.
- **Nightly churn** — Nova markup, ESM modules, and theme IDs change frequently.
- **macOS capture** — Screen Recording + Accessibility; window compositing quirks.

We are not abandoning the program — we **narrow automation to what scales** and keep manual capture for high-friction foxfooding states.

## Surfaces (17 shots)

| # | Shot | Tier | What it captures |
|---|------|------|------------------|
| 1 | chrome | automated | Default Nova chrome on a loaded page |
| 2 | sidebar | automated | Sidebar open (bookmarks) |
| 3 | vertical-tabs | automated | Vertical tab strip |
| 4 | tab-grouping | best_effort | Tab groups (chrome script) |
| 5 | new-tab | automated ⚠️ | Nova new tab page — **blank under Marionette** (ISSUE-001) |
| 6 | private-window | automated | Private browsing window |
| 7 | smart-window | automated ⚠️ | Smart Window on `about:newtab` — same NTP blocker as 05 |
| 8 | search | automated | Urlbar focused with query |
| 9 | first-run | automated | About Welcome / onboarding |
| 10 | continuous | automated | Deferred / continuous onboarding |
| 11 | settings-account | automated | Settings — Account section |
| 12 | customize-toolbar | automated | Customize Toolbar mode |
| 13 | chrome-dark | **manual** | Default Dark theme — selected tab fill |
| 14 | sidebar-history-empty | automated | History sidebar empty state |
| 15 | vertical-tabs-overflow | automated | Vertical tabs scroll overflow |
| 16 | tab-grouping-collapsed | **manual** | Collapsed tab group |
| 17 | chrome-youtube-background | automated | YouTube in background tab |

## Outputs

- `captures/YYYY-MM-DD__<version>/` — PNGs + `manifest.json`
- `.state/last-run.json` — last successful run metadata

## Run manually

**Daily automated tier (14 shots):**

```bash
./setup/bin/run-nightly-nova-screenshots.sh
```

**Include best-effort tab grouping:**

```bash
./setup/bin/run-nightly-nova-screenshots.sh --include-best-effort
```

**Force automation to try manual-tier shots (may warn):**

```bash
./setup/bin/run-nightly-nova-screenshots.sh --include-manual
```

**Then complete manual checklist** for 13 and 16 unless you used `--include-manual` and accepted warnings.

```bash
python3 -m pd_os.cli nightly-nova-screenshots --dry-run
python3 -m pd_os.cli nightly-nova-screenshots --only chrome,new-tab
```

## Schedule

Daily via launchd (`com.pd-os.nightly-nova`). Install:

```bash
./setup/launchd/install-nightly-nova.sh
```

The scheduled job runs **automated tier only**. Add manual PNGs after the run or weekly.

## macOS permissions

First run must be from **Terminal.app** (not Cursor's agent shell):

```bash
cd ~/VibeCoding_BK/work/pd-os
./setup/bin/run-nightly-nova-screenshots.sh
```

Grant both to **Terminal**:

- **Screen Recording** — `screencapture` window capture
- **Accessibility** — optional fallback only

System Settings → Privacy & Security.

If you see **"System access is required"** / `--remote-allow-system-access` in the terminal, update pd-os (the launcher now passes that flag automatically) and re-run.

If you see **"damaged or incomplete"**, `/Applications/Firefox Nightly.app` is broken — usually a **stuck update** (missing `Contents/Info.plist`). Open Nightly from Finder to finish updating, reinstall, or set `firefox_binary` in `shots.json` to a local `obj-*/dist/Nightly.app` build.

Preflight (runs automatically):

```bash
./setup/bin/check-nightly-capture-prereqs.sh
```

After a successful run, sync PNGs to FigJam:

```bash
# Writes data/projects/.../.state/figjam-pending.json (also runs automatically via --sync-figjam)
./setup/bin/run-nightly-nova-screenshots.sh

# Then in Cursor: ask to "sync nightly captures to FigJam"
```

FigJam board: see `figjam.json` for `file_url` and placeholder node IDs.

## Config

Edit `shots.json` to adjust prefs, wait times, `automation` tier, or Firefox path. Base Nova prefs:

- `browser.nova.enabled`
- `browser.newtabpage.activity-stream.nova.enabled`
- `browser.urlbar.quicksuggest.ampTopPickUseNovaIconSize`
- `browser.smartwindow.enabled`
