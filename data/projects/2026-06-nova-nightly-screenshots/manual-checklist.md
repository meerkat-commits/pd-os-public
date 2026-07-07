# Manual capture checklist

Shots marked `"automation": "manual"` in `shots.json` are **not** run by the daily script. Marionette cannot reliably force these chrome states on macOS Nightly + Nova.

**Time:** ~2–3 minutes total. Drop PNGs into the same dated folder as the automated run (`captures/YYYY-MM-DD__<version>/`).

---

## 13 — chrome-dark (`13-chrome-dark.png`)

**Test case:** TC-CH-06 — selected tab fill in Default Dark theme  
**Preconditions:** Nova on (`browser.nova.enabled`)

1. Quit Nightly completely (Cmd+Q).
2. Open **Firefox Nightly** (use the same profile you use for foxfooding, or a fresh profile with Nova prefs from `shots.json`).
3. **Settings → Appearance → Themes → Dark** (built-in Dark, not Alpenglow).
4. Open `https://example.com` with one tab selected.
5. Confirm tab strip is **dark** Nova chrome (not light lavender/red stripes).
6. Screenshot the window → save as `13-chrome-dark.png`.

**Fail if:** Light theme chrome, wrong selected-tab fill vs Figma.

---

## 16 — tab-grouping-collapsed (`16-tab-grouping-collapsed.png`)

**Test case:** TC-CH-04 — horizontal group collapse hairline direction  
**Preconditions:** Horizontal tabs (not vertical); `browser.tabs.groups.enabled` on

1. Open three tabs: `example.com`, `mozilla.org`, `example.org`.
2. Select **mozilla.org** and **example.org** → right-click → **Add tabs to new group** → label **QA**.
3. Collapse the **QA** group (click group label/chevron).
4. Select **example.com** so it is the foreground tab (group stays collapsed).
5. Screenshot → save as `16-tab-grouping-collapsed.png`.

**Fail if:** Hairline collapses from both edges; wrong tab foreground; group not collapsed.

**Note:** Animation direction needs manual review or screen recording — static PNG is for collapsed state only.

---

## Optional — 04 tab-grouping (`04-tab-grouping.png`)

Tier **best_effort** — script may attempt this with `--include-best-effort`. If the PNG looks wrong, capture manually:

1. Same three tabs as above.
2. Group all three into **QA**, leave expanded.
3. Screenshot → `04-tab-grouping.png`.

---

## After manual captures

1. Copy PNGs into today’s `captures/YYYY-MM-DD__<version>/` folder (same as automated run).
2. Optionally append to `manifest.json` with `"status": "manual"` or re-run with `--only chrome-dark,tab-grouping-collapsed` knowing automation may still warn.
