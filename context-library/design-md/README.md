# DESIGN.md collection (agent-facing)

Plain-text design specs in the spirit of [awesome-design-md](https://github.com/VoltAgent/awesome-design-md) and Google Stitch’s `DESIGN.md` idea: drop a file into context and ask an agent to match the UI.

## Entries

| Entry | Use when |
|-------|----------|
| [`nova-classic/`](nova-classic/README.md) | **Project Nova desktop** — tab strip, chrome, NTP, settings; [`DESIGN.md`](nova-classic/DESIGN.md) + Cursor skill `nova-classic` |
| [`firefox-mobile-android/`](firefox-mobile-android/README.md) | **Gecko / Fenix** Android: [`DESIGN.md`](firefox-mobile-android/DESIGN.md), [`preview.html`](firefox-mobile-android/preview.html) (phone-frame catalog), build notes |
| [`x.ai-inspired/`](x.ai-inspired/README.md) | **xAI-like** stark monochrome, monospace display type, brutalist minimalism — same idea as [getdesign.md/x.ai](https://getdesign.md/x.ai/design-md); includes vendored `DESIGN.md` + usage |

## Maintenance

Fenix tokens live in the **mozilla-mobile/firefox-android** monorepo (e.g. `android-components/components/ui/colors/.../photon_colors.xml`, Fenix `res/values`). Refresh hex or semantic names when you bump branches; this folder is a **stable agent summary**, not a build artifact.
