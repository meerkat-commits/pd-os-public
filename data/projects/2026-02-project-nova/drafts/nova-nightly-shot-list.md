# Nova Nightly — screenshot shot list

**Project:** [Project Nova](../brief.md)  
**Build:** Firefox Nightly (Daily)  
**Matrix:** macOS · Windows · Linux × Light · Dark  
**Last updated:** 2026-06-26

**Naming:** `{nn}-{shot-id}__{platform}__{theme}.png`  
(e.g. `01-chrome__macos__light.png`)

**Prefs reference:** `browser.nova.enabled` · `browser.newtabpage.activity-stream.nova.enabled` · `browser.smartwindow.enabled` · `sidebar.revamp`

---

## Core (17)

| ID | File | Surface | State |
| :---- | :---- | :---- | :---- |
| 01 | `01-chrome` | Classic Window | `https://example.com`, one tab selected |
| 02 | `02-sidebar` | Sidebar | Bookmarks panel open |
| 03 | `03-vertical-tabs` | Vertical tabs | `sidebar.verticalTabs=true` |
| 04 | `04-tab-grouping` | Tab groups | 3 tabs, group **QA**, expanded |
| 05 | `05-new-tab` | Nova New Tab | `about:newtab` |
| 06 | `06-private-window` | Private Window | `about:privatebrowsing` |
| 07 | `07-smart-window` | Smart Window | Signed in; New Smart Window |
| 08 | `08-search` | Urlbar | Focused; query `firefox nova` |
| 09 | `09-first-run` | Onboarding | Fresh profile; About Welcome |
| 10 | `10-continuous` | Onboarding | Post-first-run profile |
| 11 | `11-settings-account` | Settings | `about:preferences#sync` |
| 12 | `12-customize-toolbar` | Customize toolbar | Customize mode active |
| 13 | `13-chrome-dark` | Chrome (dark) | Dark theme; `example.com`, one tab |
| 14 | `14-sidebar-history-empty` | Sidebar | History panel, empty state |
| 15 | `15-vertical-tabs-overflow` | Vertical tabs | 15+ tabs, scrolled |
| 16 | `16-tab-grouping-collapsed` | Tab groups | Group **QA** collapsed |
| 17 | `17-chrome-youtube-background` | Media tab | YouTube background tab; `example.com` foreground |

---

## Extended (10)

| ID | File | Surface | State |
| :---- | :---- | :---- | :---- |
| B01 | `b01-app-menu` | Application menu | Menu open |
| B02 | `b02-switcher-menu` | Classic Window / Smart Window switcher | Switcher open |
| B03 | `b03-urlbar-hover` | Urlbar | Shield or star hovered |
| B04 | `b04-tab-mute-hover` | Tab chrome | Mute control hovered (YouTube tab) |
| B05 | `b05-settings-appearance` | Settings | `about:preferences#general` → Appearance |
| B06 | `b06-about-logins` | Credential management | `about:logins` |
| B07 | `b07-sidebar-synced-tabs` | Sidebar | Synced tabs panel |
| B08 | `b08-smart-window-switch` | Mode switch | Classic Window → Smart Window via switcher |
| B09 | `b09-horizontal-tabs-many` | Horizontal tabs | 12+ tabs, horizontal layout |
| B10 | `b10-private-plus-classic` | Cross-mode | Classic Window · Private Window · Smart Window |

---

## Optional (8)

| ID | File | Surface | State |
| :---- | :---- | :---- | :---- |
| C01 | `c01-ntp-wallpaper-bold` | Nova NTP | Bold wallpaper variant |
| C02 | `c02-ntp-widgets` | Nova NTP | Widgets visible |
| C03 | `c03-side-panel-ai` | AI side panel | Panel open |
| C04 | `c04-download-progress` | Toolbar | Download in progress |
| C05 | `c05-hcm` | Chrome | High contrast mode |
| C06 | `c06-compact-density` | Chrome | Compact mode; horizontal tabs |
| C07 | `c07-customize-switcher-removed` | Customize toolbar | Switcher removed from toolbar |
| C08 | `c08-fullscreen` | Chrome | Fullscreen |

---

## Edge cases (suggested)

Grouped by where regressions tend to show up. Not all apply every drop — pick by milestone or when touching that surface.

### Chrome & layout

| ID | File | Surface | State |
| :---- | :---- | :---- | :---- |
| E01 | `e01-chrome-maximized` | Chrome | Window maximized; horizontal tabs |
| E02 | `e02-chrome-narrow` | Chrome | Window ~1024px wide; tab strip compression |
| E03 | `e03-horizontal-tabs-overflow` | Horizontal tabs | 12+ tabs; strip overflow / scroll |
| E04 | `e04-pinned-tabs-vertical` | Vertical tabs | Pinned tabs row; empty pin state |
| E05 | `e05-multiple-tab-groups` | Tab groups | 2+ groups; one collapsed, one expanded |
| E06 | `e06-split-view` | Chrome | Split view; two panes, focus in each |
| E07 | `e07-fullscreen-dom` | Chrome | Page DOM fullscreen (video/player) |
| E08 | `e08-toolbar-overflow` | Toolbar | Enough toolbar items to overflow chevron |

### Sidebar & panels

| ID | File | Surface | State |
| :---- | :---- | :---- | :---- |
| E09 | `e09-sidebar-collapsed` | Sidebar | Launcher only; panel closed |
| E10 | `e10-sidebar-right` | Sidebar | Sidebar docked right |
| E11 | `e11-vertical-tabs-narrow` | Vertical tabs | Collapsed/narrow vertical strip width |
| E12 | `e12-vertical-tab-group-collapsed` | Vertical tabs | Tab group collapsed in vertical layout |
| E13 | `e13-synced-tabs-empty` | Sidebar | Synced tabs panel, empty |
| E14 | `e14-synced-tabs-error` | Sidebar | Synced tabs panel, error state |
| E15 | `e15-extensions-panel` | Chrome | Extensions panel open |
| E16 | `e16-etp-panel` | Chrome | Protections / ETP popover open |

### Urlbar & search

| ID | File | Surface | State |
| :---- | :---- | :---- | :---- |
| E17 | `e17-urlbar-zero-results` | Urlbar | Query with no suggestions |
| E18 | `e18-urlbar-quicksuggest` | Urlbar | Query triggering quick suggest row |
| E19 | `e19-find-in-page` | Chrome | Find bar open over content |

### Modes & cross-surface

| ID | File | Surface | State |
| :---- | :---- | :---- | :---- |
| E20 | `e20-smart-window-private` | Smart Window | Private Window (if supported in build) |
| E21 | `e21-ntp-signed-out` | Nova NTP | Signed out; sign-in CTA visible |
| E22 | `e22-about-logins-unlock` | Credential management | `about:logins` primary-password prompt |
| E23 | `e23-settings-payments-edit` | Settings | Payments → Edit card dialog |
| E24 | `e24-text-selection-chatbot` | Content + chrome | Text selected; chatbot affordance visible |

### Theme & accessibility

| ID | File | Surface | State |
| :---- | :---- | :---- | :---- |
| E25 | `e25-system-theme-auto` | Chrome | Appearance → System theme (auto) |
| E26 | `e26-forced-colors` | Chrome | OS high contrast / forced colors |
| E27 | `e27-increased-contrast` | Chrome | `browser.display.use_document_colors` / contrast prefs on |

### Platform-specific

| ID | File | Surface | State |
| :---- | :---- | :---- | :---- |
| E28 | `e28-win-switcher-placement` | Chrome | Windows — switcher left of window controls |
| E29 | `e29-mac-switcher-placement` | Chrome | macOS — switcher upper right |
| E30 | `e30-linux-gtk-titlebar` | Chrome | Linux — note GTK vs in-chrome titlebar in filename |

### Transient (screenshot may need video)

| ID | File | Surface | State |
| :---- | :---- | :---- | :---- |
| E31 | `e31-private-tab-flash` | Private Window | New private tab first paint |
| E32 | `e32-vertical-group-animation` | Vertical tabs | Tab group expand/collapse mid-motion |
| E33 | `e33-download-complete` | Toolbar | Download animation / completed state |

---

## Counts

| Set | Shots |
| :---- | :---- |
| Core × 3 platforms × 2 themes | 102 |
| Extended × 3 × 2 | 60 |
| Optional × 3 × 2 | 48 |
| Edge cases × 3 × 2 (if full matrix) | 198 |
