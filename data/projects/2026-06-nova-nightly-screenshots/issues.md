# Nova nightly screenshots — issues

**Project:** `2026-06-nova-nightly-screenshots` · **Updated:** 2026-06-24

---

## ISSUE-001 — Nova NTP blank under Marionette (shots 05, 07) — RESOLVED 2026-06-25

| Field | Value |
|-------|--------|
| **Status** | **Resolved** — hybrid no-marionette capture (Option B) |
| **Severity** | P1 (primary surface; punch-QA shot 05) |
| **Shots** | `new-tab` (05), `smart-window` (07, same `about:newtab` URL) |
| **First seen** | 2026-06-24 (Nightly 154.0a1) |
| **Fixed in** | 2026-06-25 (Nightly 154.0a1) |

### Resolution

Implemented Option B (hybrid capture). Shots flagged `requires_no_marionette: true` and `automation: "hybrid"` in `shots.json` are now:

1. Launched **without** `-marionette` / `-remote-allow-system-access` so Activity Stream is not gated by Firefox automation mode.
2. Launched via **direct binary** (`subprocess.Popen([firefox_binary, ...])`) instead of `open -na`, which was silently dropping `-no-remote`/`-profile` flags on some startups.
3. Routed straight to `about:newtab` at launch (previously `_launch_url_for_shot` rewrote NTP URLs to `about:blank` for the Marionette-deferred path — now only applied when Marionette is in use).
4. Given a longer wait budget (12s + 1.5s post-focus settle) to cover cold-start + Activity Stream React mount.

Marionette is still used for every other shot — chrome, sidebar, vertical tabs, search, etc. — so no regression to those.

Code: `pd_os/nightly_screenshots.py` — `ShotSpec.requires_no_marionette`, `_launch_firefox_process`, `_launch_url_for_shot`, `capture_shot` hybrid branch.

### Original symptom (kept for posterity)

### Symptom (pre-fix)

Automated `05-new-tab.png` showed **empty dark content** (chrome + Marionette urlbar stripes only). Manual capture in normal Nightly showed full Nova NTP: sidebar, search, top sites, widgets.

### Root cause

**Marionette is designed to suppress Activity Stream / New Tab Page** for test stability. On `-marionette` connect, Firefox applies recommended testing prefs (e.g. `browser.newtabpage.enabled: false`, `browser.topsites.contile.enabled: false`, `browser.discovery.enabled: false`). Marionette does not override prefs already in `user.js`, and we set `browser.newtabpage.enabled: true` there — but **Nova NTP still does not hydrate** in the automation profile.

Debug (`setup/bin/debug-ntp-capture.py`, 2026-06-24):

- After `start_session()`, prefs read `True` for `browser.newtabpage.enabled` and `browser.newtabpage.activity-stream.nova.enabled`.
- `navigate("about:newtab")` → `document.readyState: complete`, `body` present, **`innerText.length: 0`** — empty shell, no search bar or top sites in DOM.
- Same for `about:home`.

This is not a capture-timing bug; screen capture faithfully records what Marionette-mode Firefox renders.

### Attempted fixes (did not resolve)

1. `browser.newtabpage.enabled: true` in `user.js` / `shots.json` `base_prefs`
2. `set_prefs()` + re-navigate after Marionette session
3. Launch on `about:blank`, defer `about:newtab` until post-session
4. `browser.newtabpage.activity-stream.testing.shouldInitializeFeeds: true`
5. Longer waits + stricter NTP ready checks (manifest now reports `warning` honestly)

### Recommended resolutions (pick one)

| Option | Effort | Notes |
|--------|--------|-------|
| **A. Manual tier** for 05 (+ 07) | Low | Add to `manual-checklist.md`; ~30s per shot |
| **B. Hybrid capture** | Medium | Marionette for other shots; launch **without** `-marionette` for NTP-only capture |
| **C. Warm seeded profile** | Medium–high | Pre-populate topsites/widgets; fragile across Nightly updates |
| **D. Firefox-side spike** | Unknown | Force Activity Stream re-init post-session; no proven path yet |

### References

- Marionette: [Bug 1506643](https://bugzilla.mozilla.org/show_bug.cgi?id=1506643) — disable `about:newtab` in automation
- Marionette: [Bug 1996347](https://bugzilla.mozilla.org/show_bug.cgi?id=1996347) — `shouldInitialize` / feed gating for WebDriver
- Code: `pd_os/nightly_screenshots.py` — `_ensure_nova_newtab`, `_NTP_READY_SCRIPT`
- QA: `qa-test-cases.md` — shot map row `new-tab`

---

## ISSUE-002 — Tab grouping best-effort unreliable (shot 04)

| Field | Value |
|-------|--------|
| **Status** | Open — expected for tier |
| **Severity** | P2 |
| **Shot** | `tab-grouping` (04) |
| **Manifest signal** | `expected 3 tabs, got 1`; `no tab groups created` |

Chrome-scope tab open + group scripts do not reliably create grouped tabs on Nightly 154. Shot remains **`best_effort`**; use `--include-best-effort` optionally. Collapsed state is **manual** (shot 16).

---

## ISSUE-003 — Dark theme + collapsed groups (shots 13, 16)

| Field | Value |
|-------|--------|
| **Status** | Accepted — manual tier by design |
| **Severity** | P1 surfaces, manual capture |
| **Shots** | `chrome-dark` (13), `tab-grouping-collapsed` (16) |

Built-in Dark theme and collapsed tab-group selection do not stick under Marionette. See `manual-checklist.md`.

---

## ISSUE-004 — FigJam sync incomplete for shots 11–17

| Field | Value |
|-------|--------|
| **Status** | Open — low |
| **Severity** | P3 |
| **Detail** | `figjam.json` has placeholder node IDs for shots 01–10 only; 11–17 need node mapping before auto-sync |

---

## ISSUE-005 — Cursor agent shell cannot capture

| Field | Value |
|-------|--------|
| **Status** | Accepted — workflow constraint |
| **Severity** | P3 (ops) |
| **Detail** | Cursor’s integrated terminal lacks Screen Recording. Runs must use **Terminal.app** (`check-nightly-capture-prereqs.sh` enforces). Agent can launch batch via `osascript` → Terminal. |

---
