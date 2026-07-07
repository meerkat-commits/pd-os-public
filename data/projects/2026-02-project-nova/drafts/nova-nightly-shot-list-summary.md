# Nova Nightly screenshot program — executive summary

## What this is

A standardized shot list for capturing Project Nova UI from **Firefox Nightly (Daily)** across **macOS, Windows, and Linux**, in **light and dark** chrome. It gives release engineering and design a shared catalog of surfaces and states — same names, same matrix — for release notes, stakeholder reviews, and visual regression.

## Why it matters

Nova spans **Classic Window**, **Private Window**, **Smart Window**, sidebar, NTP, onboarding, settings, and credential management. Without a fixed shot list, captures drift by platform, theme, and reviewer. This document defines **what** to photograph, not **how** — the release team owns capture workflow.

## Scope

| Dimension | Coverage |
| :---- | :---- |
| **Platforms** | macOS · Windows · Linux |
| **Themes** | Light · Dark (built-in) |
| **Surfaces** | Classic Window · Private Window · Smart Window, tabs (horizontal + vertical), sidebar, NTP, urlbar, onboarding, settings, customize, logins |

## Shot tiers

| Tier | Shots | Full matrix (×3 platforms ×2 themes) | Role |
| :---- | :---- | :---- | :---- |
| **Core** | 17 | **102** | Baseline Nova experience — minimum per milestone |
| **Extended** | 10 | 60 | Menus, hovers, mode switch, cross-surface parity |
| **Optional** | 8 | 48 | Wallpaper, widgets, AI panel, compact/HCM, fullscreen |
| **Edge cases** | 33 | 198 | Layout stress, empty/error states, platform-specific chrome, a11y |

## Core set at a glance

Classic Window · Private Window · Smart Window · sidebar · vertical tabs · tab groups · Nova NTP · urlbar search · first-run & continuous onboarding · settings · customize toolbar · dark theme · history empty · tab overflow · collapsed groups · media tab.

## Edge cases (high value)

Maximized/narrow window, horizontal overflow, split view, sidebar collapsed/right, synced-tabs empty/error, platform switcher placement (Win vs Mac), forced colors/HCM, signed-out NTP, payments dialog, transient states (private-tab flash, animations) where video may be needed.

---

## Edge cases (suggested)

Grouped by where regressions tend to show up. Not all apply every drop — pick by milestone or when touching that surface.

**Chrome & layout** — maximized window, narrow width (~1024px), horizontal tab overflow, pinned tabs (vertical), multiple groups, split view, DOM fullscreen, toolbar overflow.

**Sidebar & panels** — launcher-only collapsed state, sidebar on right, narrow vertical strip, vertical group collapsed, synced tabs empty/error, extensions panel, ETP popover.

**Urlbar** — zero-result query, quick suggest row, find-in-page bar open.

**Modes** — Private Window (Smart Window, if in build), signed-out NTP, `about:logins` unlock, payments edit dialog, text-selection chatbot affordance.

**Theme & a11y** — system theme (auto), forced colors / HCM, increased contrast prefs.

**Platform** — switcher placement shots scoped to Windows vs macOS (decision-dependent); Linux GTK titlebar note.

**Transient** — private tab first-paint flash, vertical group animation, download animation — may need video rather than PNG.

Several map directly to foxfooding cases (launcher–panel gap, overflow fade, dark selected-tab fill, purple flash, etc.) that the core 17 don’t cover.

**Full shot tables:** [`nova-nightly-shot-list.md`](nova-nightly-shot-list.md)
