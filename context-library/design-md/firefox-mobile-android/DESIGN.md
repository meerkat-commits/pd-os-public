# DESIGN.md — Firefox for Android (Fenix on Gecko)

**Product**: Firefox for Android (Fenix)  
**Platform**: Android (GeckoView; coexists with Material system patterns)  
**Purpose**: Agent-readable visual and interaction language for mocks, prototypes, and specs—not a substitute for the engineering theme source of truth.

**Verify against**: [mozilla-mobile/firefox-android](https://github.com/mozilla-mobile/firefox-android) (`photon_colors.xml`, Fenix `res/values/colors.xml`, Compose/Material theme where applicable). Values below reflect Photon scales used in that tree; names may differ per resource alias.

**Same folder (PD-OS)**:

| File | Role |
|------|------|
| [`README.md`](README.md) | How to use this bundle, links to upstream |
| [`preview.html`](preview.html) | Static dark-chrome + private-accent **visual reference** (Roboto; not shipping UI) |

---

## 1. Visual theme and atmosphere

- **Feel**: Capable, calm, privacy-forward. The browser UI stays **quiet** so web content and the user’s task stay primary.
- **Density**: Comfortable for one-handed use; avoid cramming chrome. Prefer **clear hierarchy** over decoration.
- **Brand**: Firefox leans **Genuine** (clear, grounded) in product UI; **Playful** and **Fiery** show up in selective moments (onboarding, campaigns, strong warnings)—not in every label.
- **Light vs dark**: Firefox Android supports both; **dark chrome** is common for browsing. Specs should call out theme explicitly.
- **Private mode**: Distinct **purple / violet** accent thread (separate from default theme) so state is obvious at a glance.

---

## 2. Color palette and roles

Photon uses stepped scales (10–90) for most hues. Prefer **semantic roles** in UI, not raw step numbers, unless you are matching engineering resources.

### Core brand hues (approximate hex from Photon scales)

| Role | Typical use | Reference hex | Notes |
|------|-------------|---------------|--------|
| **Primary blue** | Links, primary actions, key focus | `#0060DF` | Blue 60 on Photon blue scale |
| **Primary blue (pressed / dark)** | Pressed states, darker emphasis | `#0250BB`–`#054096` | Deeper blues on same scale |
| **Accent violet** | Highlights, private mode, brand moments | `#592ACB`, `#AB71FF` | Violet scale; lighter tints for glows/gradients |
| **Ink / neutral text** | Body text on light surfaces | `#15141A`–`#2B2A33` range | “Ink” neutrals for readability |
| **Grey surfaces (light)** | Cards, sheets, dividers | `#F9F9FA`, `#E0E0E6`, `#CFCFD8` | Light grey steps |
| **Grey surfaces (dark)** | Dark chrome backgrounds | `#2B2A33`, `#23222B`, `#15141A` | Dark grey / ink-like surfaces |
| **Success / positive** | Confirmations, safe states | Teal/green scale (e.g. `#2AC3A2` region) | Use sparingly in chrome |
| **Warning** | Caution, non-destructive alerts | Yellow/orange scale | Avoid relying on color alone |
| **Error / destructive** | Errors, destructive actions | `#E22850`, `#FF4F5E` region | Pair with icon + copy |
| **Scrim / overlay** | Modals, menus over content | Black with alpha (e.g. ~32–60% opacity) | Keep content legible |

### Semantic guidance

- **Default browsing**: Blue for **links and primary actions**; neutrals for structure.
- **Private browsing**: Lead with **violet** for accents and key affordances so mode is unmistakable.
- **Don’t**: Rainbow chrome; heavy gradients on every surface; low-contrast grey-on-grey body text.

---

## 3. Typography

- **Platform reality**: Android defaults to **Roboto** / **Noto** for CJK where applicable. Fenix may use bundled UI fonts in some layers (e.g. Inter in newer Compose surfaces)—**match the current app** when implementing, not this doc alone.
- **Hierarchy**:

| Level | Usage | Weight | Sizing guidance |
|-------|--------|--------|------------------|
| **Display / title** | Toolbar titles, major headings | Medium–SemiBold | Larger than body; avoid ultra-bold blocks of text |
| **Body** | Descriptions, settings | Regular | Default reading size; comfortable line length |
| **Caption / meta** | URLs, timestamps, hints | Regular | Smaller; still meet contrast |
| **Button label** | Text inside buttons | Medium (often) | All caps only if Material pattern demands; Firefox product copy prefers sentence case for longer labels |

- **Rules**: Prefer **sentence case** for product strings; **plain language**; avoid tiny legal-grey copy for critical warnings.

---

## 4. Component styling

### Toolbar / top chrome

- Flat or subtle elevation; **one clear primary action** (e.g. menu or identity) where relevant.
- URL / identity area should feel **trustworthy**: clear lock or security affordances when applicable.

### Buttons

- **Primary**: Filled, high contrast (blue or theme primary).
- **Secondary**: Text button or outlined; still meets touch target size.
- **Destructive**: Red/error hue; require confirmation for irreversible actions.

### Cards and rows

- Settings and lists: **row height** comfortable for touch; optional dividers or spacing—not both cluttering.
- Icons: **simple, monochrome** toolbar icons unless illustrating a feature; use `fx_mobile_icon_color_primary`-style semantics (icon tint follows theme).

### Inputs

- Touch-friendly fields; clear error states (color + text + optional icon).
- Respect **keyboard and IME**: avoid hiding the primary action behind the keyboard without scroll.

### Sheets, dialogs, menus

- **Modal**: scrim + clear title, primary/secondary actions.
- **Bottom sheets**: good for contextual actions on Android; keep options scannable.

### Tabs and navigation

- Bottom navigation or tab strip should reflect **current task** clearly; avoid duplicate nav metaphors in one view.

---

## 5. Layout principles

- **Spacing**: Use a **4 dp / 8 dp** mental grid (Material baseline); align Firefox-specific padding to existing Fenix components when possible.
- **Thumb reach**: Primary actions in **lower half** when one-handed; avoid-only top-corner critical actions without alternative.
- **Content first**: Chrome minimizes vertical theft; scrollable content gets priority.
- **Locales**: Allow **string growth** (German, etc.); no fixed-width labels that truncate critical meaning.

---

## 6. Depth and elevation

- Android Material: elevation shadows on sheets/FABs; Firefox chrome often **flatter** than heavy Material marketing UIs.
- Use **elevation for interaction layers** (FAB, snackbar, modal), not for every card.
- **Private mode** may use subtle tint or gradient shifts—keep **readable contrast** for text and icons.

---

## 7. Do’s and don’ts

### Do

- Pair **color with text or icon** for state (error, success, private).
- Write for **people**, not “users”; short, direct strings.
- Respect **TalkBack** and font scaling; touch targets **≥ 48 dp** effective where possible.
- Default to **clarity** over ornament.

### Don’t

- Don’t rely on **fox puns** in dense settings UI; voice skill applies—light touch.
- Don’t use **pure color** as the only signal for privacy or security.
- Don’t mirror **desktop Firefox** 1:1; mobile has different constraints and patterns.
- Don’t ship **wall-of-settings** without grouping and progressive disclosure.

---

## 8. Responsive behavior and Android specifics

- **Orientations**: Phone portrait primary; landscape should not break critical flows (toolbar, URL, primary CTA).
- **Foldables / tablets**: Consider two-pane settings or wider content where Fenix already patterns it.
- **System integration**: Status bar, nav bar, and **edge-to-edge** behavior follow Android version and Fenix theme—call out safe areas in specs.
- **Gestures**: Back gesture, overscroll, and **pull-to-refresh** (where applicable) should not fight custom gestures.
- **Web content**: The page is not “Firefox themed”—**chrome** is; don’t force site content to match Photon.

---

## 9. Agent prompt guide

Quick anchors for “build this like Firefox Android”:

- **Background (dark chrome)**: deep neutral `#15141A` / `#23222B` family; **text** light grey/white with strong contrast.
- **Primary action / link**: `#0060DF` blue family on light; on dark, use theme-adjusted primary (often lighter blue or violet per theme).
- **Private accent**: `#592ACB` / `#AB71FF` violet accents, distinct from default session.
- **Error**: `#E22850` / `#FF4F5E` with explicit message.
- **Shape**: Moderate corner radius on cards/buttons (Material-influenced); not ultra-pill unless matching a specific Fenix component.
- **Tone**: Genuine, concise; playful only where the brief says welcome/onboarding.

**Example prompt fragment**:  
“Android phone UI, Firefox for Android dark theme, Photon blues and violet for private mode, 8 dp spacing, 48 dp touch targets, sentence case, minimal chrome, Material-style bottom sheet for actions.”

---

## 10. Voice alignment (product copy)

For strings and microcopy, align with Firefox brand voice: **Genuine**, **Playful**, **Fiery**—weighted by surface (see `context-library/brands/firefox_voice.md` and Firefox brand messaging docs). Product UI defaults to **Genuine**; marketing-style punch belongs in campaigns, not error dialogs.

---

## 11. Implementation guide (from this DESIGN.md)

Use this section when turning the spec into **layouts, themes, or prototypes**. Shipping **Firefox for Android** must still follow **`firefox-android`** resources and code review; treat snippets below as **mocks / side projects / agent starters** unless you are merging into Mozilla’s tree.

### 11.1 How to implement

1. **Lock theme**: Say “dark chrome” vs “light” vs **private** (violet thread) before building pixels.
2. **Pull colors** from §2; **pull spacing and targets** from §5 and §7 (8 dp grid, ≥48 dp touch).
3. **Match components** to §4 (toolbar, primary/secondary/destructive, lists, sheets).
4. **Cross-check** [`preview.html`](preview.html) for relative contrast and hierarchy (same-folder reference).

### 11.2 Dark chrome — layout tokens (preview-aligned)

These hex values match the PD-OS `preview.html` mock so **markdown + HTML stay in sync** for agents.

| Token | Hex | Typical use |
|-------|-----|-------------|
| Chrome base | `#15141A` | Screen background, content under toolbar |
| Toolbar / elevated surface | `#2B2A33` | Top toolbar, bottom sheet surface |
| URL bar / inset field | `#32313C` | Toolbar URL field background |
| Text primary (on dark) | `#FBFBFE` at ~96% opacity equivalent | Headings, row titles |
| Text secondary | white ~72% opacity | Subtext, URL placeholder |
| Divider / hairline | white ~6–8% opacity | List separators, toolbar bottom edge |
| Primary button | `#0060DF` | Filled CTA (normal browsing) |
| Primary pressed | `#0250BB` | Pressed / darker emphasis |
| Private primary | `#592ACB` | Filled CTA in private mode (with lighter violet for links/highlights `#AB71FF` as needed) |
| Error / destructive text | `#E22850` | Destructive actions (pair with label + confirmation) |
| Positive / secure hint | `#2AC3A2` | e.g. connection “good” dot (never alone for safety) |

Corner radii in the preview: **4 dp** small, **8 dp** controls, **12 dp** sheets/device frame—Material-adjacent, not pills unless the product pattern demands it.

### 11.3 Android XML (prototype `res/values/colors.xml`)

Use **`photon_*` / Fenix names** in a real Gecko build. For a **standalone prototype**, you can namespace names to avoid clashes:

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <!-- Prototype-only: rename / merge with photon_* when importing into firefox-android -->
    <color name="fx_proto_chrome_base">#15141A</color>
    <color name="fx_proto_toolbar">#2B2A33</color>
    <color name="fx_proto_url_bar">#32313C</color>
    <color name="fx_proto_primary">#0060DF</color>
    <color name="fx_proto_primary_pressed">#0250BB</color>
    <color name="fx_proto_private_primary">#592ACB</color>
    <color name="fx_proto_private_accent_light">#AB71FF</color>
    <color name="fx_proto_error">#E22850</color>
    <color name="fx_proto_success">#2AC3A2</color>
</resources>
```

Reference in layouts with `@color/fx_proto_primary`, then replace with upstream `@color/photonBlue60` (or current Fenix alias) when integrating with Fenix.

### 11.4 Jetpack Compose (prototype `Color` objects)

```kotlin
import androidx.compose.ui.graphics.Color

object FirefoxMobileDarkPrototype {
    val ChromeBase = Color(0xFF15141A)
    val Toolbar = Color(0xFF2B2A33)
    val UrlBar = Color(0xFF32313C)
    val PrimaryBlue = Color(0xFF0060DF)
    val PrimaryBluePressed = Color(0xFF0250BB)
    val PrivatePurple = Color(0xFF592ACB)
    val PrivateVioletLight = Color(0xFFAB71FF)
    val Error = Color(0xFFE22850)
    val Success = Color(0xFF2AC3A2)
}
```

Wire these into `MaterialTheme` (`colorScheme` / custom extension) or a small `FxChromeTheme { }` wrapper; for Fenix, prefer existing theme types in the app module.

### 11.5 Gecko / Fenix checkout

- Build and theme work live in **[mozilla-mobile/firefox-android](https://github.com/mozilla-mobile/firefox-android)** (Fenix + Android Components), not in PD-OS.
- After changing visuals in-tree, update **this `DESIGN.md`** only when you want the **agent-facing summary** to stay aligned with what shipped (optional maintenance).

---

## 12. Disclaimer

This document is a **design companion for humans and coding agents**. Trademarks and visual identities belong to their owners. For shipping code, use **in-repo Android resources and Compose themes** as the source of truth.
