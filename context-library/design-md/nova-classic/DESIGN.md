# DESIGN.md — nova-classic

Design reference for AI agents, designers, and engineers making changes to this Firefox desktop UI prototype.
Ground truth is the CSS in `index.html`, `newtab.html`, and `settings.html`. When in doubt, read those files.

---

## 1. Product context

**What this is.** nova-classic is a high-fidelity HTML/CSS prototype of a redesigned Firefox desktop browser UI. It covers the full browser chrome: tab strip, toolbar, address bar, sidebar, side panels, new tab page, settings, and a multi-step onboarding flow.

**Who it is for.** Firefox users on desktop — primarily Windows and macOS — who want a browser that feels personal, calm, and trustworthy. The design supports German (DE) and North American (NA) locales.

**What users need to accomplish:**
- Open and navigate between tabs quickly.
- Access bookmarks, history, passwords, synced tabs, and AI chatbots from a sidebar without leaving the current page.
- Personalise the new tab page (wallpaper, widgets, shortcuts, feed topics).
- Configure browser appearance and settings.
- Complete a short onboarding flow to sign in and pick a theme.

**Design principles visible in the implementation:**
- **Calm, not noisy.** Surfaces use whitespace generously. Hover states are subtle (4–6% opacity darken). Nothing screams for attention.
- **Purple with warmth.** The primary brand colour is deep violet `#7845e8`, but it lives alongside warm cream `#fcf5f0` and the lavender-to-peach gradient on the tab strip. This combination is intentional and should not be replaced with a flat neutral palette.
- **Soft geometry.** Almost every interactive element is fully pill-shaped (`border-radius: 9999px`). Panels and popovers use `16px` radius. Content areas use `4px`. Never mix these — the hierarchy of rounding signals element type.
- **Motion confirms, doesn't decorate.** Transitions are `0.15s` for micro-interactions and `0.28s` for layout shifts. There are no decorative animations.

---

## 2. Visual design principles

### Aesthetic direction
Polished but not corporate. Warm lavender tones, soft shadows with a purple tint, and frosted-glass cards on the new tab page. The overall feeling should be closer to a creative productivity tool than a utility app.

### Layout and spacing
- The browser window sits 10px from the viewport edge on all sides (`margin: 10px` on `.browser-window`).
- Internal chrome padding is 5px (`padding: 5px` on `.browser-window`). Chrome elements — tab strip and toolbar — are 44px tall with 6px inner padding.
- Side panels open to 322px. The AI chatbot panel opens to 400px. The sidebar icon rail opens to 44px.
- Gap between sidebar and content area: 6px (`margin-right: 6px`).
- New tab content max-width: 920px, centred, with `82px 48px 80px` padding (top, sides, bottom).
- Section gaps on the new tab page: 32px.
- Popovers use 8px internal padding consistently.

### Typography
- **Font stack:** `system-ui, -apple-system, "Segoe UI", "Helvetica Neue", Arial, sans-serif` (via `--font`). No web fonts are loaded.
- **Size scale in use:**
  - 10px — badge labels, VPN label, unit suffixes
  - 11px — secondary metadata, subheaders in menus, zoom value
  - 12px — tab title, sidebar panel headings (`.hp-title`), bookmark titles, section labels
  - 13px — body text everywhere: menu items, panel body, form labels, CTA buttons in panels
  - 14px — AI provider list items, settings body text
  - 15px — address bar input, primary CTA buttons, sign-in button
  - 16px — empty-state titles, AI modal title
  - 17px — new tab section titles
  - 22px — new tab brand wordmark, timer display
  - 26px — onboarding heading
- **Weight:** 400 regular, 500 medium (shortcuts label, timer tabs), 590 semibold (CTAs, panel titles, toolbar buttons), 600 bold (folder labels, new tab section titles, settings nav).
- **Line height:** `line-height: normal` for single-line UI labels; `1.4`–`1.45` for body copy that wraps.

### Colour usage

All tokens are defined in `:root` and duplicated at the top of each HTML file:

| Token | Value | Use |
|---|---|---|
| `--color-primary` | `#7845e8` | Buttons, links, active states, focus rings, toggles |
| `--color-primary-hover` | `#6936d8` | Primary button hover |
| `--color-button-text` | `#3e217e` | Ghost button text (sign-in, skip) |
| `--color-button-border` | `rgba(194,79,255,0.4)` | Ghost button border |
| `--color-text` | `#15141a` | Default body text |
| `--color-text-secondary` | `#25052c` | Slightly warmer dark, used for headings |
| `--color-text-muted` | `rgba(21,20,26,0.69)` | Supporting text |
| `--color-text-disabled` | `rgba(21,20,26,0.4)` | Inactive/placeholder text |
| `--color-bg-cream` | `#fcf5f0` | Browser window background, onboarding left pane |
| `--color-border-panel` | `rgba(33,3,64,0.2)` | Chrome top border |
| `--color-border-secondary` | `#e1e3f2` | Address bar, search field borders |
| `--color-border-content` | `#bfbfc9` | Content area, sidebar, side panel borders |
| `--color-border-tab` | `#b397ff` | Unused as a utility; tab active border is a gradient |

Dark mode surfaces (applied via `body.dark-mode`):
- Window/outer background: `#210340` (deep purple)
- Toolbar, sidebar, content area surfaces: `#181820`
- Popovers: `#1c1726`
- Text primary: `#f5f3fb`; muted: `rgba(245,243,251,0.55–0.7)`
- Borders: `rgba(255,255,255,0.1–0.15)`

Do not add new colour values outside this set. If a new surface needs a colour, use one of the existing tokens or a documented opacity variant of `#15141a` or `#7845e8`.

### Gradients
- **Tab strip (light):** `linear-gradient(163deg, rgb(245,236,255) 40%, rgb(255,237,224) 100%)` — lavender to warm peach
- **Tab strip (dark):** `linear-gradient(163deg, rgb(42,36,61) 40%, rgb(69,50,51) 100%)`
- **Active tab border:** `linear-gradient(45deg, #bba0ff 0%, #ff8d5b 71%)` — the signature purple-to-orange gradient used on the active tab and gradient dividers
- **Progress bar / onboarding fill:** `linear-gradient(155deg, rgb(187,160,255) 21%, rgb(255,141,91) 79%)`
- **Smart Window icon:** `linear-gradient(-31deg, rgb(255,54,71) 5%, rgb(117,67,227) 97%, rgb(255,152,14) 130%)`

### Radius, borders, shadows, elevation

| Token / class | Value | Used on |
|---|---|---|
| `--r-circle` | `9999px` | All icon buttons, tabs, address bar, CTAs, inputs |
| `--r-xl` | `16px` | Ghost buttons (sign-in, skip), popovers, most panels |
| `--r-xxl` | `24px` | Large primary CTA on onboarding |
| `4px` (hardcoded) | — | Chrome-top, content area, sidebar, side-panel rounded rect |
| `8px` (hardcoded) | — | Browser window outer shell, bookmark edit input, AI providers |
| `12px` (hardcoded) | — | Menu items inside panels (acct, etp, vpn row items), VPN illustration |
| `14px` (hardcoded) | — | New tab cards, widgets |
| `16px` (hardcoded) | — | Popovers (etp-panel, vpn-panel, acct-panel, bm-panel, ext-panel, am-panel, ws-panel) |
| `--shadow-chrome` | `0 0 14px rgba(115,56,226,0.24)` | Chrome-top unit, open sidebar, open side panels |
| `--shadow-window` | `0 0 20px rgba(0,0,0,0.1)` | Browser window shell |
| Popover shadow | `0 0.375px 1.5px rgba(0,0,0,0.02), 0 3px 12px rgba(0,0,0,0.05–0.1)` | All dropdown popovers |

The purple-tinted shadow (`--shadow-chrome`) is a deliberate brand expression. Do not substitute it with a neutral grey shadow on chrome-level elements.

### Iconography
- All icons are inline SVG or `<img src=".svg">` at 16×16px. No icon font.
- Icons in toolbar buttons (`.tb`) and sidebar buttons (`.sidebar-btn`) are 16×16.
- Popovers use 16×16 icons for menu items and 24×24 for action icons.
- In dark mode, raster/PNG icons inside chrome (`.tb img`, `.sidebar-btn img`) are inverted using `filter: brightness(0) invert(1) opacity(0.75)`. On hover, opacity increases to 0.95.
- Do not apply this inversion filter to branded/coloured icons (favicons, AI provider logos, Firefox icon). Those must stay full colour.
- Setting icons in the settings sidebar are 16×16 SVG files in `assets/settings-*.svg`.

---

## 3. Component rules

### Toolbar button (`.tb`)
32×32px circle, transparent background, 1px solid transparent border. Hover: `rgba(0,0,0,0.06)` fill. Active/engaged: `rgba(120,69,232,0.12)` fill. Selected (e.g., sidebar open): `rgba(120,69,232,0.14)` fill. Use `.active` for toggled-on state; use `.selected` for the currently-chosen item in a switcher context.

### Address bar (`.address-bar`)
Full-width flex container, 32px height, `border-radius: 20px`, `border: 1px solid var(--color-border-secondary)`. On focus-within: `border-color: #7845e8; box-shadow: 0 0 0 2px rgba(120,69,232,.12)`. Input text is `font-size: 15px`, colour `var(--color-text-disabled)` at rest to indicate it's a placeholder URL.

### Tabs (`.tab`)
32px height, `border-radius: 9999px`, width 232px default, max 380px, min 64px. Inactive tabs are transparent with no border. Active tab uses the gradient border trick: `background: linear-gradient(white, white) padding-box, linear-gradient(45deg, #bba0ff 0%, #ff8d5b 71%) border-box; border: 1px solid transparent`. Never use a solid colour border on an active tab. Tab title truncates with ellipsis.

### Sidebar icon rail (`.chrome-sidebar`)
44px wide when open. Closed state: `width: 0; opacity: 0`. Opens with a smooth width+opacity transition. Icon buttons are `.sidebar-btn` at 32×32 pill. Settings button is pinned to the bottom via `margin-top: auto` on `.sidebar-settings`. The sidebar can be positioned left or right via `body.sidebar-right` class which reverses the flex direction.

**Attached mode:** when `.chrome-sidebar.attached`, the sidebar merges visually with the adjacent side panel by removing the shared border and using `clip-path` to suppress the shadow bleed. Do not change the `clip-path` values — they are tuned to prevent a visible gap or double-shadow.

### Side panels (`.side-panel`)
322px wide when open (AI chatbot panel: 400px). Closed: `width: 0; opacity: 0`. Same cubic-bezier transition as the sidebar. Internal padding: 12px. Panel header is `.hp-header` with a 12px bold title and icon buttons (24×24) for close/actions. Search fields inside panels use `.hp-search`: pill shape, 32px, focus ring matches address bar.

### Popovers
All toolbar popovers (ETP, VPN, Account, Bookmarks, Extensions, Window Switcher, App Menu) share the same shell: `border-radius: 16px; padding: 8px; border: 1px solid #d7d8e3; box-shadow: 0 0.375px 1.5px rgba(0,0,0,0.02), 0 3px 12px rgba(0,0,0,0.05)`. Widths vary (276–384px). The `.open` class toggles them from `display: none` to `display: flex`. An invisible full-screen overlay (`.overlay.open`) closes the panel on outside click.

### Menu items inside popovers
`.am-item`, `.acct-item`, `.etp-menu-item`, `.ws-item` all follow the same pattern: `display: flex; align-items: center; gap: 8px; padding: 6–8px; border-radius: 10–12px; transition: background 0.12–0.15s`. Hover: `rgba(0,0,0,0.04–0.06)`. Selected: `rgba(123,97,143,0.3)`. 13px font, #14092b text, no text-decoration.

### Primary CTA button
Two sizes. Large (onboarding): `min-height: 48px; padding: 12px 24px; font-size: 15px; border-radius: var(--r-xxl)`. Small (panel/sidebar): `min-height: 32px; padding: 8px 20px; font-size: 13px; border-radius: 9999px`. Both use `background: var(--color-primary); color: white; font-weight: 590`. Hover: `background: var(--color-primary-hover)` plus optional box-shadow `0 4px 12px rgba(120,69,232,.3)` on large variant only.

### Ghost button
Used for "Sign in", "Skip", cancel actions. `background: transparent; border: 1px solid var(--color-button-border); color: var(--color-button-text); border-radius: var(--r-xl); padding: 4px 16px; min-height: 32px; font-size: 15px; font-weight: 590`. Hover: `background: rgba(120,69,232,0.05)`.

### Inputs (`.bm-input`, `.hp-search input`, `address-bar input`)
All inputs suppress the browser default outline (`outline: none`) and implement a custom focus ring via `border` or `box-shadow`. Standard focus: `border: 2px solid #7529e8`. Never rely on the browser's default `:focus` outline.

### Checkboxes (`.sp-check`, `.pers-check`)
Custom appearance via `appearance: none`. 16×16, `border-radius: 4px`. Checked: `background: var(--color-primary); border-color: var(--color-primary)`. Checkmark rendered via `::after` with a CSS rotated rectangle. Use this pattern consistently — do not use native checkboxes in the UI.

### Toggle switch (`.pers-toggle`, `.etp-toggle`)
30×18px pill, `background: #cfcad6` off, `background: var(--color-primary)` on. Dot is 14×14px, positioned with `left: 2px` off / `left: 14px` on, animated with `transition: left 0.15s`. State stored via `aria-checked="true/false"`.

### Segmented control (`.pers-seg`, `.seg-control`)
Pill container in `#f3eff8`, buttons inside are transparent by default. Active button: `background: #e5dcf6; border: 1px solid var(--color-primary)`. All buttons share `border-radius: 9999px` with 3px container padding.

### Cards (new tab page: `.newtab-card`, `.widget`)
`background: rgba(255,255,255,0.92); backdrop-filter: blur(12px); border-radius: 14px; box-shadow: 0 1px 4px rgba(0,0,0,0.06)`. Hover on cards: `transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.1)`. The frosted glass effect (`backdrop-filter`) is intentional — do not replace with solid white.

### Empty states (`.hp-empty`, `.pw-empty`)
Illustration centred at top (typically 220×222px SVG), then a title at 16px, then body text at 13px, then a primary CTA button. Empty state illustration files are in `assets/` (e.g., `history-empty.svg`, `passwords-empty.svg`, `tabs-empty.svg`, `sync-empty.svg`). The widget empty slot uses a dashed border: `border: 1px dashed rgba(21,20,26,0.3); background: rgba(255,255,255,0.35)`.

### Settings page
Left sidebar (`.st-sidebar`) with a search field, nav items (`.st-nav-item`) using icon + label, and an "Extensions and themes" external link at the bottom. Nav items are plain links with hover `rgba(0,0,0,0.04)` and active uses a primary colour left indicator or background. Main content (`.st-main`) uses `.st-card` containers with `h3` section headings and option grids (`.st-option-grid`) for visual pickers.

---

## 4. Interaction patterns

### Navigation
- Clicking a sidebar button toggles the corresponding side panel and marks the button `.active`. Only one panel can be open at a time.
- The sidebar itself is toggled by a toolbar button. Closing the sidebar also closes any open panel.
- The sidebar can be "attached" (no gap between sidebar and panel, shared border removed) via `.chrome-sidebar.attached`.
- Pages (newtab, settings, etc.) are simulated by showing/hiding regions inside `.content-area`, not by actual navigation.

### Hover, focus, active states

| Element | Hover | Focus | Active/Selected |
|---|---|---|---|
| Toolbar button (`.tb`) | `rgba(0,0,0,0.06)` bg | Purple focus ring | `rgba(120,69,232,0.12)` bg |
| Sidebar button | `rgba(0,0,0,0.06)` bg | — | `rgba(120,69,232,0.14)` bg |
| Menu item | `rgba(0,0,0,0.04–0.06)` bg | — | `rgba(123,97,143,0.3)` bg |
| Search/address bar | — | `border-color: #7845e8; box-shadow: 0 0 0 2px rgba(120,69,232,.12)` | — |
| Primary button | `#6936d8` bg | Purple ring | `#5a2bc2` bg |
| Ghost button | `rgba(120,69,232,0.05)` bg | — | — |
| Shortcut icon | `transform: scale(1.05)` | — | — |
| New tab card | `translateY(-2px) + deeper shadow` | — | — |

### Animations and transitions
- **Micro-interactions** (hover fill, border colour): `0.15s` linear or ease.
- **Mode/theme colour changes**: `0.3s` ease (background, text colour, border).
- **Sidebar/panel open-close**: `width 0.28s cubic-bezier(0.42,0,0.58,1), opacity 0.22s cubic-bezier(0.42,0,0.58,1)`. The opacity trails width so the element fades out before fully collapsing. Do not change this easing — it matches the browser's expected physics.
- **Personalize panel slide-in**: `transform: translateX(16px); opacity: 0` → `translateX(0); opacity: 1` with the same easing.
- **Progress bar fill**: `transition: width 0.4s ease`.
- **Bookmark folder chevron**: `transform: rotate(-90deg)` when collapsed, `transition: transform 0.2s ease`.
- **Tab strip background**: `transition: background 0.35s` — slightly slower than other transitions to feel weighted.

There are no CSS keyframe animations in this codebase. If you need to add one, justify it.

### Disclosure patterns
- Folder collapse in bookmarks panel: toggle `.collapsed` class on `.bm-folder`. The chevron rotates -90° via CSS transform. Children hide via `display: none` on `.bm-folder.collapsed > .bm-items`.
- Popovers: controlled by adding `.open` class to both the overlay and the panel element. The overlay is a fixed inset-0 element that blocks pointer events and closes the popover on click.
- Side panels: controlled by `.open` class; width+opacity animate to 0/322px.

---

## 5. Accessibility rules

### Keyboard behaviour
- All interactive elements must be reachable by Tab. The current codebase uses `<button>` and `<a href="#">` elements throughout — do not replace them with `<div onclick>`.
- Icon-only buttons carry `title` attributes and/or `aria-label` (e.g., `title="Close passwords"`, `aria-label="Toggle folder"`).
- Decorative icons carry `aria-hidden="true"`.
- Side panels set `aria-hidden="true"` when closed and must be toggled to `"false"` when open (already implemented in JS).

### Focus states
The native `:focus` outline is suppressed (`outline: none`) everywhere. Every interactive element must implement a visible custom focus indicator. The standard ring is: `border-color: #7845e8; box-shadow: 0 0 0 2px rgba(120,69,232,0.12)`. Do not remove focus styles for "aesthetic" reasons.

### Contrast
- Body text `#15141a` on white: > 18:1. Acceptable.
- Muted text `rgba(21,20,26,0.69)` on white: ~7:1. Acceptable for secondary text.
- Disabled text `rgba(21,20,26,0.4)` on white: ~4:1. Marginal — use only for truly disabled/inactive states, not for supporting copy.
- Primary purple `#7845e8` on white for interactive links: ~5:1. Acceptable for large/bold text; verify for small link text.
- Do not use `color: rgba(20,9,43,0.7)` or lighter for text that carries information users need to act on.

### Semantic structure
- Settings: uses `<aside>` for the nav sidebar and `<main>` for the content area.
- Settings page title is `<h2>`, section headings are `<h3>`. Maintain this hierarchy.
- Panel titles (`.hp-title`) are `<div>` — they are OK for prototype purposes but should become `<h2>` or `<h3>` in production.
- Lists in the VPN panel use `<ul><li>` correctly.

### Motion sensitivity
All transitions are `0.15–0.4s`. There are no looping animations or auto-playing motion. If a `prefers-reduced-motion` media query is added, at minimum set `transition-duration: 0.01ms` for sidebar/panel width/opacity transitions.

---

## 6. Responsive behaviour

### Breakpoints defined
| Breakpoint | Rule |
|---|---|
| `max-width: 1100px` | New tab feed changes from 3-column (`1.2fr 1fr 1.2fr`) to 2-column (`1fr 1fr`), third column spans full width |
| `max-width: 900px` | Onboarding left pane (fox illustration) hides; right pane goes full width. New tab widgets collapse to 1 column; feed collapses to 1 column; horizontal padding reduces to 20px |
| `max-height: 680px` | Onboarding: fox illustration shrinks from 351px to 280px wide; heading shrinks from 26px to 22px; gap compresses from 24px to 16px |

### Minimum/maximum widths
- Tabs: `min-width: 64px; max-width: 380px; width: 232px` default.
- Side panels: fixed at 322px — they don't flex. At narrow viewport sizes the panel will overlap the content area.
- New tab content: `max-width: 920px`, no minimum set. Content will compress below 920px.
- Browser window: `calc(100% - 20px)` — always fills the viewport minus 10px margin on each side.

### Overflow
- `.browser-window` uses `overflow: clip`.
- `.content-area` uses `overflow: hidden`.
- Sidebar and side panels use `overflow: hidden` while closed and transition to visible when open.
- Scrollable regions (bookmark list, settings nav, personalize panel body) use `overflow-y: auto` with a styled scrollbar: `width: 6px; background: rgba(0,0,0,0.15); border-radius: 3px`.

### Component collapse behaviour
- Sidebar can be moved from left to right via `body.sidebar-right` — it does not collapse to a bottom bar.
- The new tab brand logo and weather widget are `position: absolute` and stay pinned to corners regardless of content scroll.
- The personalize panel slides in from the right as an overlay inside `.newtab-area` — it never stacks vertically.

---

## 7. Content and tone

### Naming conventions
- Settings category: sentence case, noun phrases ("Account and sync", "Privacy and security", not "ACCOUNT AND SYNC" or "Manage your account").
- Panel titles: short nouns ("Bookmarks", "Passwords", "Tabs from other devices").
- Button labels: verb phrases for primary actions ("Sign in", "Continue", "Import from file"), noun for dismiss ("Close").
- Onboarding headings are question-free statements of benefit, not instructions ("Your Firefox, your way", not "Do you want to customise Firefox?").

### Label style
- All UI labels use sentence case. No ALL CAPS except the VPN "VPN" badge label.
- Menu shortcuts use the platform shorthand format (e.g., "⌘W", "Ctrl+W"), right-aligned in the menu item.
- Section headers in panels are 13px `font-weight: 600` — they are labels, not headings.

### Empty state language
Pattern: **Short title** (what happened or what this is) + **Body** (brief context or benefit) + **CTA** (one primary action).
Examples from the codebase:
- "Save your passwords to a safe spot" → no body → "Import from file" + "Sign into sync"
- "From laptop to phone, seamlessly" → "Keep your browsing connected across devices…" → "Sign in"
- Empty state body copy uses em-dashes (`&mdash;`) for asides, not parentheses.

### Error and loading states
Not explicitly implemented in this prototype. When adding: use the same body text size (13px) and muted text colour `rgba(21,20,26,0.69)`. Error text should be concise and actionable. Avoid "Something went wrong" with no next step.

### Things to avoid in copy
- "Please" — the UI doesn't beg.
- Technical jargon in user-facing labels (e.g., "Render process" should be "Browser process").
- Sentence-ending periods on single-line labels and button text.
- Exclamation marks except in marketing contexts (not present here).

---

## 8. Do / Don't examples

### ✅ DO: Use the gradient border for the active tab
```css
/* Correct active tab */
.tab.active {
  background: linear-gradient(white, white) padding-box,
              linear-gradient(45deg, #bba0ff 0%, #ff8d5b 71%) border-box;
  border: 1px solid transparent;
}
```
```css
/* WRONG — kills the signature gradient border */
.tab.active {
  background: white;
  border: 1px solid #7845e8;
}
```

### ✅ DO: Use pill radius for all interactive buttons
```css
/* Correct */
.my-btn { border-radius: 9999px; }
```
```css
/* WRONG — mixes radius hierarchy, looks out of place next to tabs and address bar */
.my-btn { border-radius: 6px; }
```

### ✅ DO: Animate sidebar with the cubic-bezier timing
```css
/* Correct */
transition: width 0.28s cubic-bezier(0.42,0,0.58,1), opacity 0.22s cubic-bezier(0.42,0,0.58,1);
```
```css
/* WRONG — ease-in feels sluggish for layout shifts */
transition: width 0.3s ease-in;
```

### ✅ DO: Keep popover shadows neutral, chrome shadows purple-tinted
```css
/* Chrome-level shadow (sidebar, panel, chrome-top) */
box-shadow: 0px 0px 14px rgba(115, 56, 226, 0.24);

/* Popover shadow (menus, dropdowns) */
box-shadow: 0 0.375px 1.5px rgba(0,0,0,0.02), 0 3px 12px rgba(0,0,0,0.05);
```
Don't use the purple shadow on popovers — they float above the chrome and should feel lighter.

### ✅ DO: Invert dark-mode icons with a filter, not separate dark-mode SVGs
```css
body.dark-mode .tb img {
  filter: brightness(0) invert(1) opacity(0.75);
}
body.dark-mode .tb:hover img {
  filter: brightness(0) invert(1) opacity(0.95);
}
```
Exception: branded and coloured icons (favicons, AI logos, Firefox logo, sidebar-sparkles) must use `filter: none !important`.

### ✅ DO: Use the body class pattern for layout variants
```css
/* Sidebar on the right */
body.sidebar-right .main-area { flex-direction: row-reverse; }

/* Dark mode */
body.dark-mode .toolbar { background: #181820; }
```
Do not create separate HTML files for layout variants. Use class modifiers on `<body>`.

### ❌ DON'T: Add a new root-level colour outside the token set
If you find yourself writing `background: #4a90d9` or any colour not in the token table above, stop. Derive the colour from an existing token or add a new token with justification.

### ❌ DON'T: Use `display: none / display: flex` directly for panel show/hide without the matching opacity transition
The pattern requires both `.open` to change `width`/`opacity` and the panel to already have `display: flex` in its base styles. Toggling `display` alone produces a flash without the smooth transition.

### ❌ DON'T: Give new tab cards a solid white background
```css
/* WRONG — loses the frosted-glass effect that ties the card to the wallpaper */
.newtab-card { background: white; }

/* Correct */
.newtab-card { background: rgba(255,255,255,0.92); backdrop-filter: blur(12px); }
```

### ❌ DON'T: Place a fox illustration or mascot in any panel or surface not currently using one
The fox/mascot SVGs are used only in: onboarding left pane, ETP panel card, VPN panel illustration, and the checklist widget. These are intentional emotional moments. Adding the fox elsewhere dilutes it.

---

## 9. Implementation guidance

### Where key components live

| Component | File | Selector / section |
|---|---|---|
| Browser window shell + chrome-top | `index.html`, `newtab.html`, `settings.html` | `.browser-window`, `.chrome-top` |
| Tab strip + tabs | All three | `.tab-strip`, `.tab` |
| Toolbar + address bar | All three | `.toolbar`, `.address-bar` |
| Sidebar icon rail | All three | `.chrome-sidebar`, `.sidebar-btn` |
| Side panels (history, bookmarks, passwords, synced, AI) | `index.html`, `newtab.html` | `.side-panel`, `#historyPanel`, `#bookmarksPanel`, etc. |
| New tab page content | `newtab.html` | `.newtab-area`, `.newtab-content`, `.newtab-feed` |
| Personalize panel | `newtab.html` | `.pers-panel`, `.pers-overlay` |
| Onboarding split-screen | `index.html` | `.content-left`, `.content-right` |
| Settings page | `settings.html` | `.st-sidebar`, `.st-main`, `.st-card` |
| Toolbar popovers | `index.html`, `newtab.html` | `.etp-panel`, `.vpn-panel`, `.acct-panel`, `.bm-panel`, `.ext-panel`, `.am-panel`, `.ws-panel` |

### Design tokens
All CSS custom properties are defined inline in each file's `<style>` block under `:root`. There is no separate tokens file. If you need to update a token, update it in all three HTML files. Consider consolidating into a shared `<link rel="stylesheet">` if the project grows.

### Dark mode and theme state
- `body.dark-mode` is toggled by JS reading `localStorage.getItem('firefoxTheme')`.
- URL params `?mode=dark` or `?mode=light` can preset the mode.
- All dark-mode overrides are scoped with `body.dark-mode` as the selector prefix. Do not use `@media (prefers-color-scheme: dark)` — the prototype uses a manual toggle.

### Density support
`localStorage.getItem('firefoxDensity')` returns `'compact'` or `'standard'`. The compact layout is visualised in `assets/density-compact.svg` and `assets/density-standard.svg` (setting previews) but not yet fully implemented in CSS. When adding compact-mode styles, use `body.density-compact` as the class prefix.

### Adding a new side panel
1. Add a `<div class="side-panel" id="myPanel" aria-hidden="true">` inside `.main-area`, after the existing panels.
2. Add the corresponding `.side-panel-inner` with `.hp-header` + title + close button.
3. Add a `.sidebar-btn` entry to `.sidebar-tools` in `.chrome-sidebar`.
4. In JS, hook the sidebar button click to call the existing open/close pattern: add `.open` to the panel, set `aria-hidden="false"`, add `.active` to the sidebar button, and close any other open panel.
5. Do not set an explicit `width` on the panel in its base state — the transition requires it to start at `width: 0`.

### Keeping aligned with the design system
- CSS is co-located with HTML in `<style>` blocks — there are no external CSS files. When copying a pattern, copy the full selector including dark-mode overrides.
- The token names are descriptive and consistent. Before adding a new class, check whether an existing modifier (`.active`, `.open`, `.collapsed`, `.selected`, `.attached`) covers the state.
- All three HTML files (`index.html`, `newtab.html`, `settings.html`) share an identical `:root` token block and identical shared component styles (tab strip, toolbar, sidebar, side panels, popovers). If you change a shared component, apply the change in all three files.
