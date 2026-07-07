# Case study: Project Nova

Role: Director, Mobile & AI UX · Nova UX lead  
Timeline: 2026 company priority · In Nightly  
Scope: Chrome, new tab, onboarding, settings. Parallel with Smart Window and mobile.

---

## Stakes

Firefox has to feel like it belongs in 2026 and still feel like home. Nova is the company-priority redesign (chrome, new tab, onboarding, settings) while Smart Window and mobile surfaces move in parallel.

We're not chasing a trend board. We're making Firefox feel modern, inviting, and familiar at the same time.

---

## The call

- Parallel modes, not a takeover. Classic Firefox for most people; AI Mode opt-in for those who want it. Same token and craft discipline across both.
- Empowerment over surprise. Compact mode returns in Appearance settings. Switcher is on by default but removable via Customize Toolbar. User opt-out, not product removal.
- Platform-specific chrome, consistent rules. Switcher anchors left of window controls on Windows, upper right on macOS. App menu icon does not move between Classic, Smart, and Private windows.

---

## Trade-offs we documented

- Icon refresh deprioritized. Not a Nightly ship blocker.
- Tab border gradient: ship without if a quick fix doesn't land.
- Hover contrast accepted at 3:1 with team-aligned risk on the record.
- Touch mode explicitly not scoped for Nova MVP.
- Reload/stop toolbar animation removed; bookmark animation deferred post-Nova.

---

## Proof

- Ship status: In Nightly; public feedback on Reddit and Mozilla Connect.
- Token trajectory: NTP CSS propagation 28% to 77.5% (Feb 2025 to Jun 2026). Nova NTP font-size on token scale: 98.5%.
- Community signal: Verified in-thread Mozilla replies; community impact tracker.
- Decision hygiene: 13+ cross-team decisions logged with owners, evidence links, and explicit trade-offs.

### Public quotes (safe to cite)

> "Even the current version in Nightly looks so much better than any previous Firefox design." (Mozilla Connect)

> "Compact mode is officially coming back? Oh my god. Thank you." (Reddit)

---

## Artifacts

- [Community impact landing page](https://shimmering-mochi-6b0645.netlify.app/)
- [Reddit: Sharing more about Project Nova](https://www.reddit.com/r/firefox/comments/1tjk5pv/sharing_more_about_project_nova/)
- Nightly + craft slides: `draft/image-manifest.md` → `site/assets/firefox/`
- Decision table excerpt (3 rows max on public site)

### Sample decision rows (public-safe)

| Decision | Call | Trade-off |
|----------|------|-----------|
| Switcher placement | Left of window controls (Windows); upper right (macOS) | Do not move other chrome elements |
| App menu consistency | Icon must not move between Classic, Smart, Private | (none) |
| Compact mode | In Appearance settings, not customize toolbar | (none) |

---

## If the conversation goes wider

| Topic | Pivot |
|-------|-------|
| "Another redesign?" | Proton was 2021; Nova is cohesion + empowerment, not churn for its own sake |
| Performance | Graphics and performance testing; delight doesn't trade off speed |
| Vertical space / compact | Compact mode is the lever; early Nightly isn't final compact tuning |
| AI takeover fears | Classic stays Firefox; AI Mode is opt-in on Mozilla's terms |

---

## PD-OS sources

- `data/projects/2026-02-project-nova/brief.md`
- `data/projects/2026-02-project-nova/drafts/nova-decision-registry-rows.md`
- `data/projects/2026-02-project-nova/dashboard-design-tokens.md`
- `data/projects/2026-06-nova-podcast/drafts/nova-podcast-outline-v3.md`
