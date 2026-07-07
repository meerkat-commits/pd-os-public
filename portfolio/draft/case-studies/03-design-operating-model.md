# Case study: AI-native design operating system

Public title (not "AI velocity mandate")  
Role: Director, Mobile & AI UX  
Timeline: 2026 H2  
Scope: 35-person hybrid org; ~15-person product design core as velocity proof layer

---

## Stakes

Leadership needed to know design could move faster with AI — and that design, partners, and eng could all be AI-native builders at scale. They also needed one owner for product design execution on Nova: standards, monthly proof, partner handoffs.

The answer isn't 3x Figma files. It's an operating system for how a hybrid org generates with AI, gates by discipline, and proves ship or decision. We pilot on the product design core and spread through pillar leads and agency on shared rules.

---

## The operating system (four layers)

| Layer | What | Who it touches |
|-------|------|----------------|
| Program | Nova + Smart Window ship discipline: decision registry, punch QA, public feedback | Whole Firefox 2026 bet |
| Triad | Design / Eng / PM gates by artifact type; partner co-create | Cross-functional handoffs |
| Org capability | Team skills hub, design-md, critique prep, agency on same contract | 35-person hybrid org |
| Velocity proof | QA backlog, builder enablement at scale, code-native patterns | ~15 product designers first |

---

## The call: three bets

| Bet | Priority | What | Proof bar |
|-----|----------|------|-----------|
| QA and close the loop | Now | Punch QA on Nova + one backlog for visual gaps. Papercuts post-Nightly. | Gaps closed from single queue; issues caught pre-ship |
| Faster calls | Ongoing | Tactical (&lt;48h, reversible) to fast signal. Strategic to deep qual. | Fast signal changed a decision |
| Code, not slides | Stretch | Runnable prototypes in Firefox tree, linked in sprint/ticket | Eng-used prototypes when team already ships in code |

### Punch severity (Nova builds)

| Level | Meaning |
|-------|---------|
| Blocker | Must fix before wider exposure |
| Fix before exposure | Should fix; don't ship as-is |
| Accept and track | Known gap. Log it and move on. |

### Tactical vs strategic

| | Tactical (fast call) | Strategic (deep qual) |
|---|----------------------|------------------------|
| What | Reversible UI/flow; single segment; answerable in &lt;48h | Big bet; trust/privacy/new-user risk |
| Method | AI-moderated / UserTesting-style fast signal | Full qual |
| Proof | Signal changed the decision | Documented why fast signal was insufficient |

### Triad gates (org-wide)

Anyone can generate with AI. Discipline owners gate. Proof is ship or decision.

| Discipline | Owns | Human gate |
|------------|------|------------|
| Design | UX intent, craft, a11y/content readiness | Ship as-is / fix / accept and track |
| Engineering | Feasibility, correctness, merge/release risk | r? + land (or block) |
| PM | Scope, priority, success criteria | In sprint / not now / success bar |

---

## Trade-offs: what we won't count

- Loom or local HTML with no eng ticket / sprint link
- "We ran a test" with no decision change
- Punch findings scattered across Jira and GitHub with no owner
- Figma labeled "prototype" when Eng needed runnable code
- Paper-cut pilot before Nova in Nightly (~post-July timing)
- New standing meetings or headcount-reduction framing

---

## Operating rules

- Discipline owners gate craft. Partners co-create. Everyone builds with AI.
- Human Eng `r?` on any product code (paper-cut pilot).
- Monthly proof to leadership: shipped/unblocked, one decision-quality case, throughput trend, one risk + mitigation, next month's single bet.
- Pillar leads (Mobile, Desktop AI, E2E) socialize standards.

---

## Proof

- Shareable brief and operating rules (public version)
- Jira snapshot as throughput proxy (trend chart; no board IDs on public site)
- Monthly format: 5 bullets, no new standing meeting
- Team skills hub merged upstream; design-md agent-readable specs

---

## Artifacts

See **`draft/image-manifest.md`**.

- Operating rules one-pager (this case study + `brief.shareable.md`)
- `site/assets/operating-model/four-layers.png`, `three-bets.png`, `pd-os-dashboard.png`

---

## PD-OS sources

- `data/projects/2026-06-ai-velocity-mandate/brief.shareable.md`
- `data/projects/2026-06-ai-velocity-mandate/drafts/2026-06__velocity-operating-rules.md`
- Do not use on public site: `brief.md`, team tier audit, Raja 1:1 docs
