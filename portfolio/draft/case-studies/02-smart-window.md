# Case study: Smart Window / AI Mode

Role: Director, Mobile & AI UX  
Timeline: 2026 · Ships with Nova program gates  
Scope: Opt-in AI browsing mode, mode transitions, motion and state design

---

## Stakes

Every browser is adding AI. The risk isn't being late. It's stapling a chatbot to chrome and calling it innovation. Smart Window has to feel opt-in, trustworthy, and distinctly Firefox.

Classic Mode is still Firefox. AI Mode is for when you want the browser to carry more of the task, with consent.

---

## The call

- Three modes, one product. Private (on-device, maximum privacy). Classic (familiar Firefox; light intelligence you can ignore). AI Mode / Smart Window (context-aware assistant on Mozilla's terms).
- Design the states nobody sees. Loading, error, empty, reduced-motion, the moment after the user turns AI off. Same intentionality as hero moments.
- Greenfield token discipline. 100% font-size tokenization on AI Window surfaces. Don't invent hex when a token exists.

---

## Trade-offs

- Question the pattern before optimizing execution. Borrowed competitor curves aren't decisions.
- Motion scope cut where it didn't earn its place (reload/stop animation removed; bookmark animation deferred post-Nova).
- Spec depth where Eng needs it; exploration where alignment needs it. Not everything is eng-ready on day one.
- History resume, thinking states, and mode transitions spec'd with acceptance criteria. Not left as "Eng will figure it out."

---

## Proof

- Token posture: Smart Window / AI Window at 100% font-size tokenized (AWDTY, Jun 2026).
- Spec depth: PRD-surface-map across history, thinking states, mode transitions, reduced-motion variants.
- Program alignment: Product Review 1 (design readiness) and Product Review 2 (implemented build + UX QA) before Nightly exposure.

---

## Design principles

1. Every detail is a decision. If you can't explain why, you didn't design it.
2. Same conviction, every scale. Hover on a settings toggle gets the same care as the thinking state.
3. Design the states nobody sees. Trust lives in error, empty, and off states.
4. Question the pattern, not just the execution. Before making it prettier, ask if the pattern is right.

---

## Artifacts

- Mode diagram (Private / Classic / AI) on site
- One motion or state demo (HTML prototype or Nightly capture): add before launch
- One spec excerpt showing eng-ready acceptance criteria: redact internal ticket IDs if needed

---

## PD-OS sources

- `.cursor/skills/smart-window-design/SKILL.md`
- `.cursor/skills/smart-window-design/references/product-context.md`
- `.cursor/skills/smart-window-design/references/prd-surface-map.md`
- `data/projects/2026-02-project-nova/dashboard-design-tokens.md` (Smart Window row)
