# nova-classic — Firefox desktop design language

Agent-readable spec for **Project Nova** desktop UI (nova-classic HTML prototype): tokens, components, motion, copy rules, and do/don't patterns.

## In PD-OS

| File | Role |
|------|------|
| [`DESIGN.md`](DESIGN.md) | Full design spec (synced from skill bundle) |
| Cursor skill | `~/.cursor/skills/nova-classic/SKILL.md` — read for quick reference + prototype file map |

## HTML prototype (ground truth CSS)

Open locally from the installed skill:

```
~/.cursor/skills/nova-classic/nova-classic/index.html
~/.cursor/skills/nova-classic/nova-classic/newtab.html
~/.cursor/skills/nova-classic/nova-classic/settings.html
```

When tokens or components change, update CSS in **all three** HTML files.

## Related

- Production token artifacts: [`work/project-nova/ref/nova-tokens.json`](../../../project-nova/ref/nova-tokens.json)
- Firefox voice for product copy: [`context-library/brands/firefox_voice.md`](../../brands/firefox_voice.md)
- Mobile (separate): [`design-md/firefox-mobile-android/`](../firefox-mobile-android/README.md)

## Refresh DESIGN.md from skill bundle

If you receive an updated `nova-classic.skill`:

```bash
unzip -o ~/Downloads/nova-classic.skill -d ~/.cursor/skills/nova-classic
# flatten inner folder if needed, then:
cp ~/.cursor/skills/nova-classic/nova-classic/DESIGN.md context-library/design-md/nova-classic/DESIGN.md
```
