# Nova foxfooding — QA test cases

**Source:** [Nova Foxfooding Bug Tracker - Bugs.csv](file:///Users/brookwkatalinich/Downloads/Nova%20Foxfooding%20Bug%20Tracker%20-%20Bugs.csv)  
**Owner:** Brooke Katalinich · **Updated:** 2026-06

Test cases match foxfooding granularity: **surface + mode + element + state + steps + expected + fail signal**.

## Severity scale (visual / craft — Nova foxfooding)

Use for **Column A (Severity)** and **Column I (Launch blocker)** in the bug tracker. Optimized for visual polish, not general usability.

| Severity | Label | Definition | Launch blocker? |
|----------|-------|------------|-----------------|
| **P0** | Must-fix / ship blocker | Wrong or broken UI in a **primary surface** (chrome, tab strip, sidebar, NTP, settings shell) that makes Nova look unfinished or misrepresents the design intent at a glance. Includes spec violations called out as release criteria. | **Yes** — mark Column I |
| **P1** | High — craft degradation | Visible inconsistency with Nova spec (radius, spacing, colour token, illustration, animation) on a **high-traffic** surface. User can still complete the task. | No, unless PM/UX flags |
| **P2** | Medium — polish | Spec drift on **secondary** states (empty/error illustrations, customize mode, edge themes) or lower-traffic paths. | No |
| **P3** | Low — nice to have | Minor nits, parity with pre-Nova, or “should we?” questions without a clear spec answer. | No |

**Visibility guide** (combine with severity):

- **High:** default window, horizontal tabs, sidebar open, urlbar, selected tab, first-run
- **Medium:** customize mode, private window, overflow scroll, collapsed groups
- **Low:** rare dialogs, edge fullscreen, single-platform quirks

**Decision shortcut:** If a designer would circle it in crit → at least P1. If it’s on the punch-QA shot list → at least P1. If it blocks saying “Nova is ready” in a stakeholder review → P0.

---

## How to use

| Layer | When | Command |
|-------|------|---------|
| **Daily baseline** | Drift detection on core surfaces | `./setup/bin/run-nightly-nova-screenshots.sh` (shots 01–10) |
| **Foxfooding pass** | Bug-tracker depth | Full run or `--only settings-account,customize-toolbar,...` (shots 11–17) |
| **Manual only** | Interaction / animation / timing | Run STR below; file bugs in tracker |

**Template** (for new bugs):

```markdown
### TC-{surface}-{nn}: {title}
- Severity: P0 | P1 | P2 | —
- Surface: Chrome | Sidebar | Sidebar – Vertical tabs | Settings | Private | …
- Bug ref: {bugzilla URL or foxfooding row}
- Preconditions: browser.nova.enabled=true; {theme, density, prefs}
- Steps: 1. … 2. …
- Expected: …
- Fail if: …
- Capture: {shot id or manual}
- Automation: screenshot | interaction | compare | manual
```

---

## Shot map

| Shot ID | File | Foxfooding coverage |
|---------|------|---------------------|
| `chrome` | 01-chrome.png | TC-CH-01 baseline chrome |
| `sidebar` | 02-sidebar.png | TC-SB-01 launcher–panel gap (horizontal) |
| `vertical-tabs` | 03-vertical-tabs.png | TC-SB-02 gap (vertical), TC-VT-03 pin empty |
| `tab-grouping` | 04-tab-grouping.png | TC-CH-03 focus ring vs underline |
| `new-tab` | 05-new-tab.png | NTP Nova layout |
| `private-window` | 06-private-window.png | TC-PB-01 (static; flash needs manual) |
| `smart-window` | 07-smart-window.png | Smart Window surface |
| `search` | 08-search.png | TC-CH-03 urlbar focus ring |
| `first-run` | 09-first-run.png | Onboarding |
| `continuous` | 10-continuous.png | Deferred onboarding |
| `settings-account` | 11-settings-account.png | TC-ST-01 section highlight |
| `customize-toolbar` | 12-customize-toolbar.png | TC-CH-09 empty space |
| `chrome-dark` | 13-chrome-dark.png | TC-CH-06 selected tab fill |
| `sidebar-history-empty` | 14-sidebar-history-empty.png | TC-SB-04 empty illustration |
| `vertical-tabs-overflow` | 15-vertical-tabs-overflow.png | TC-VT-01 fade, TC-VT-02 div line |
| `tab-grouping-collapsed` | 16-tab-grouping-collapsed.png | TC-CH-04 collapse hairline |
| `chrome-youtube-background` | 17-chrome-youtube-background.png | TC-CH-02 mute radius, TC-CH-08 autoplay icon |

---

## Chrome / tab strip

### TC-CH-01: Selected tab has no shadow
- **Severity:** —
- **Surface:** Chrome
- **Bug ref:** [2049498](https://bugzilla.mozilla.org/show_bug.cgi?id=2049498)
- **Preconditions:** Nova on; one tab open
- **Steps:** 1. Open `https://example.com`. 2. Ensure tab selected.
- **Expected:** No shadow behind active tab
- **Fail if:** Visible drop shadow under selected tab
- **Capture:** `chrome`
- **Automation:** screenshot

### TC-CH-02: Mute tab uses round Nova radius
- **Severity:** —
- **Surface:** Chrome
- **Bug ref:** [2048382](https://bugzilla.mozilla.org/show_bug.cgi?id=2048382), [2047691](https://bugzilla.mozilla.org/show_bug.cgi?id=2047691)
- **Preconditions:** Nova on; tab with audible media
- **Steps:** 1. Open YouTube in background tab (see shot 17). 2. Hover mute control on tab.
- **Expected:** Circular hover/pressed hit target
- **Fail if:** Square highlight on mute affordance
- **Capture:** `chrome-youtube-background` (+ manual hover)
- **Automation:** screenshot + manual hover

### TC-CH-03: Tab group underline vs urlbar focus ring
- **Severity:** —
- **Surface:** Chrome
- **Bug ref:** [2048395](https://bugzilla.mozilla.org/show_bug.cgi?id=2048395) (Blocked)
- **Preconditions:** Nova on; tab group created
- **Steps:** 1. Create tab group. 2. Focus address bar (Cmd+L).
- **Expected:** Group underline visible; focus ring does not obscure hairline beyond spec (≤4px intrusion on macOS)
- **Fail if:** Underline fully hidden by focus ring
- **Capture:** `tab-grouping` + `search`
- **Automation:** screenshot

### TC-CH-04: Horizontal group collapse hairline direction
- **Severity:** —
- **Surface:** Chrome
- **Preconditions:** Horizontal tabs; group expanded
- **Steps:** 1. Create group. 2. Collapse via label.
- **Expected:** Hairline collapses right→left
- **Fail if:** Collapses from both left and right edges
- **Capture:** `tab-grouping-collapsed` (static); animation needs manual/video
- **Automation:** screenshot + manual for animation

### TC-CH-05: Vertical group expand/collapse animation
- **Severity:** —
- **Surface:** Chrome
- **Bug ref:** [2050186](https://bugzilla.mozilla.org/show_bug.cgi?id=2050186)
- **Preconditions:** Vertical tabs on; group created
- **Steps:** 1. Enable vertical tabs. 2. Create group. 3. Toggle collapse on label.
- **Expected:** Animation matches horizontal tab groups
- **Fail if:** Instant toggle with no animation
- **Capture:** `vertical-tabs` + manual
- **Automation:** manual / screen recording

### TC-CH-06: Selected tab fill (Default Dark)
- **Severity:** —
- **Surface:** Chrome
- **Bug ref:** [2049861](https://bugzilla.mozilla.org/show_bug.cgi?id=2049861)
- **Preconditions:** Nova on; Default Dark theme
- **Steps:** 1. Force dark theme prefs. 2. One tab selected on loaded page.
- **Expected:** Selected tab fill matches UX spec
- **Fail if:** Wrong token / contrast vs Figma
- **Capture:** `chrome-dark`
- **Automation:** screenshot

### TC-CH-07: Maximized edge click targets
- **Severity:** —
- **Surface:** Chrome
- **Bug ref:** [2038022](https://bugzilla.mozilla.org/show_bug.cgi?id=2038022)
- **Preconditions:** Nova on; window maximized
- **Steps:** 1. Maximize window. 2. Click tab strip edges and scrollbar edges.
- **Expected:** Tabs and scrollbar respond to clicks
- **Fail if:** Clicks fall through or miss targets
- **Capture:** manual
- **Automation:** manual interaction

### TC-CH-08: Media autoplay icon (Nova on vs off)
- **Severity:** —
- **Surface:** Chrome
- **Bug ref:** [2048354](https://bugzilla.mozilla.org/show_bug.cgi?id=2048354)
- **Preconditions:** YouTube in background tab
- **Steps:** 1. Foreground tab on example.com. 2. Background tab youtube.com. 3. Compare icon with `browser.nova.enabled` false.
- **Expected:** Consistent autoplay-blocked vs play icon behavior vs non-Nova
- **Fail if:** Wrong icon when Nova enabled
- **Capture:** `chrome-youtube-background`
- **Automation:** screenshot + compare run

### TC-CH-09: Customize toolbar empty space
- **Severity:** —
- **Surface:** Chrome
- **Bug ref:** [2039272](https://bugzilla.mozilla.org/show_bug.cgi?id=2039272)
- **Preconditions:** Nova on
- **Steps:** 1. Enter Customize Toolbar mode.
- **Expected:** No huge dead zone in customize sheet
- **Fail if:** Large empty region below/around toolbar items
- **Capture:** `customize-toolbar`
- **Automation:** screenshot

### TC-CH-10: AI chatbot icon radius on text selection
- **Severity:** —
- **Surface:** Chrome
- **Preconditions:** Chatbot enabled via sidebar kebab menu
- **Steps:** 1. Enable chatbot. 2. Select text on a web page.
- **Expected:** Round button affordance
- **Fail if:** Square border on selection chatbot icon
- **Capture:** manual
- **Automation:** manual

### TC-CH-11: Split view focus shift
- **Severity:** —
- **Surface:** Chrome
- **Bug ref:** [2049282](https://bugzilla.mozilla.org/show_bug.cgi?id=2049282)
- **Preconditions:** Split view active
- **Steps:** 1. Open split view. 2. Tab between panes.
- **Expected:** Panes stable; focus ring only moves focus
- **Fail if:** Views shift when focus ring switches
- **Capture:** manual
- **Automation:** manual interaction

### TC-CH-12: Fullscreen Nova borders
- **Severity:** —
- **Surface:** Chrome
- **Preconditions:** Nova on; fullscreen + DOM fullscreen
- **Steps:** 1. Enter browser fullscreen. 2. Enter DOM fullscreen on a page.
- **Expected:** Nova borders hidden or spec-compliant in fullscreen
- **Fail if:** Visible Nova border chrome in fullscreen
- **Capture:** manual (shot not yet automated)
- **Automation:** manual

### TC-CH-13: Extensions panel illustration
- **Severity:** —
- **Surface:** Chrome
- **Preconditions:** Extensions panel open
- **Steps:** 1. Open extensions panel.
- **Expected:** New Nova illustration styling
- **Fail if:** Legacy pre-Nova artwork
- **Capture:** manual (future: `extensions-panel` shot)
- **Automation:** screenshot

---

## Sidebar

### TC-SB-01: Launcher–panel gap (horizontal tabs) — P0
- **Severity:** P0
- **Surface:** Sidebar
- **Bug ref:** [2048293](https://bugzilla.mozilla.org/show_bug.cgi?id=2048293)
- **Preconditions:** Horizontal tabs; sidebar open
- **Steps:** 1. Open sidebar on loaded page.
- **Expected:** 1px divider between launcher and panel
- **Fail if:** Gap wider than 1px
- **Capture:** `sidebar`
- **Automation:** screenshot + measure

### TC-SB-02: Launcher–panel gap (vertical tabs)
- **Severity:** —
- **Surface:** Sidebar – Vertical tabs
- **Bug ref:** [2048293](https://bugzilla.mozilla.org/show_bug.cgi?id=2048293)
- **Preconditions:** Vertical tabs; sidebar open
- **Steps:** 1. Enable vertical tabs. 2. Open sidebar.
- **Expected:** 1px divider (not 2px)
- **Fail if:** 2px line or larger gap
- **Capture:** `vertical-tabs`
- **Automation:** screenshot + measure

### TC-SB-03: Sidebar search box radius
- **Severity:** —
- **Surface:** Sidebar
- **Preconditions:** Sidebar panel with search (Bookmarks/History)
- **Steps:** 1. Open sidebar panel with search field.
- **Expected:** Fully rounded (pill) search edges
- **Fail if:** Rounded-rect only
- **Capture:** `sidebar`, `sidebar-history-empty`
- **Automation:** screenshot

### TC-SB-04: History empty illustration
- **Severity:** —
- **Surface:** Sidebar
- **Preconditions:** Empty history
- **Steps:** 1. Clear history. 2. Open History sidebar.
- **Expected:** New Nova empty-state illustration
- **Fail if:** Legacy illustration
- **Capture:** `sidebar-history-empty`
- **Automation:** screenshot

### TC-SB-05: Tabs-from-devices empty/error illustration
- **Severity:** —
- **Surface:** Sidebar
- **Preconditions:** Sync empty or error state
- **Steps:** 1. Open Tabs from other devices panel in empty/error state.
- **Expected:** New illustration (pending art approval)
- **Fail if:** Legacy illustration
- **Capture:** manual
- **Automation:** screenshot

---

## Sidebar – vertical tabs

### TC-VT-01: Overflow fade uses background colour
- **Severity:** —
- **Surface:** Sidebar – Vertical tabs
- **Bug ref:** [2049500](https://bugzilla.mozilla.org/show_bug.cgi?id=2049500)
- **Preconditions:** Vertical tabs; enough tabs to scroll
- **Steps:** 1. Open 15+ tabs. 2. Scroll tab list.
- **Expected:** Top/bottom fade to sidebar launcher background colour
- **Fail if:** Shadow-based fade
- **Capture:** `vertical-tabs-overflow`
- **Automation:** screenshot

### TC-VT-02: Overflow div line colour and weight
- **Severity:** —
- **Surface:** Sidebar – Vertical tabs
- **Preconditions:** Expanded and narrow vertical modes
- **Steps:** 1. Compare overflow divider in both modes vs [Figma spec](https://www.figma.com/design/XT0eDYh4RtbMNWaYQi0efM/Chrome-Sidebar-UX-Specifications--Sprint-1-?node-id=9006-88749).
- **Expected:** Colour and stroke per spec
- **Fail if:** Wrong colour or weight
- **Capture:** `vertical-tabs-overflow`
- **Automation:** screenshot

### TC-VT-03: Pin tabs empty illustration
- **Severity:** —
- **Surface:** Sidebar – Vertical tabs
- **Preconditions:** Pin tabs empty state
- **Steps:** 1. Open pin tabs with no pinned tabs.
- **Expected:** New illustration (pending art approval)
- **Fail if:** Legacy illustration
- **Capture:** manual
- **Automation:** screenshot

---

## Settings

### TC-ST-01: Section highlight shape
- **Severity:** —
- **Surface:** Settings
- **Preconditions:** Nova on
- **Steps:** 1. Open `about:preferences`. 2. Select Account and sync.
- **Expected:** Dark purple section highlight uses Nova pill radius
- **Fail if:** Square pre-Nova highlight with gap around pill title
- **Capture:** `settings-account`
- **Automation:** screenshot

### TC-ST-02: Edit card dialog label overlap
- **Severity:** —
- **Surface:** Settings
- **Preconditions:** Nova on
- **Steps:** 1. Open `about:preferences#managePayments`. 2. Open Edit card dialog.
- **Expected:** Exp. Month / Exp. Year labels inside rounded button bounds
- **Fail if:** Titles overlap button border
- **Capture:** manual (future: `settings-payments-edit` shot)
- **Automation:** screenshot

### TC-ST-03: Compact density in Customize (legacy)
- **Severity:** —
- **Surface:** Settings / Customize
- **Bug ref:** [2023631](https://bugzilla.mozilla.org/show_bug.cgi?id=2023631)
- **Note:** Density selector moving to about:preferences per status note
- **Capture:** manual
- **Automation:** manual

---

## Private browsing

### TC-PB-01: No purple flash on new private tab
- **Severity:** —
- **Surface:** Private
- **Bug ref:** Regression from [2033037](https://bugzilla.mozilla.org/show_bug.cgi?id=2033037)
- **Preconditions:** Nova on
- **Steps:** 1. Open new Private Browsing tab. 2. Observe first paint.
- **Expected:** Background black immediately
- **Fail if:** Purple flash before black
- **Capture:** `private-window` (static); flash needs screen recording
- **Automation:** manual / screen recording

---

## Manual-only index

| ID | Issue | Why manual |
|----|-------|------------|
| TC-CH-07 | Maximized edge clicks | Interaction |
| TC-CH-10 | AI chatbot icon | Enable + select text |
| TC-CH-11 | Split view tabbing | Interaction |
| TC-CH-12 | Fullscreen borders | Mode switch |
| TC-CH-05 | Vertical group animation | Motion |
| TC-PB-01 | Purple flash | Transient (&lt;500ms) |
| TC-ST-02 | Payments Edit card | Deep settings navigation |

---

## Run commands

```bash
# Baseline (10 shots)
./setup/bin/run-nightly-nova-screenshots.sh

# Foxfooding extension (7 shots)
python3 -m pd_os.cli nightly-nova-screenshots --only settings-account,customize-toolbar,chrome-dark,sidebar-history-empty,vertical-tabs-overflow,tab-grouping-collapsed,chrome-youtube-background

# Full 17
python3 -m pd_os.cli nightly-nova-screenshots
```
