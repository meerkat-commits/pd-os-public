# Firefox for Android (Gecko) — DESIGN.md + preview

**Firefox for Android (Fenix)** on **GeckoView**: Photon palette, Material-adjacent chrome, touch-first layout. Use this bundle for mocks, specs, and agent prompts—not as a replacement for [`firefox-android`](https://github.com/mozilla-mobile/firefox-android) theme resources.

## Usage

**In PD-OS / Cursor**

- `@`-attach or paste [`DESIGN.md`](DESIGN.md) when you want UI described as Fenix / Gecko Android (use **§11** for XML / Compose implementation snippets).
- Open [`preview.html`](preview.html) in a browser for a quick visual catalog (dark chrome + normal vs private accents).

**In another repo**

Copy `DESIGN.md` to the project root (or a `docs/` folder) and instruct your assistant to follow it. Optionally copy `preview.html` for reviews.

**Engineering source of truth**

- Repo: [mozilla-mobile/firefox-android](https://github.com/mozilla-mobile/firefox-android)
- Typical paths: `android-components/components/ui/colors/.../photon_colors.xml`, Fenix `app/src/main/res/values/colors.xml`, Compose theme modules.
- Local Gecko/Fenix builds: follow your usual **mozilla-central + Firefox for Android** workflow (see Mozilla docs / your `mach` + Android checkout).

## Files

| File | Purpose |
|------|---------|
| [`DESIGN.md`](DESIGN.md) | Full agent-oriented spec; **§11 Implementation guide** has preview-aligned tokens, prototype `colors.xml`, and Compose `Color` snippets |
| [`preview.html`](preview.html) | Static **phone-frame** catalog: toolbar mock, URL bar, buttons, list rows, bottom sheet, Photon + private swatches |

### Preview

```bash
open context-library/design-md/firefox-mobile-android/preview.html
```

Roboto loads from Google Fonts on first open; layout works offline after cache.

## Disclaimer

Not an official Mozilla deliverable. Trademarks belong to their owners. Ship production UI from **in-tree Android/Compose resources**, not from this preview file.
