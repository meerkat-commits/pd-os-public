# Design critique prep — Mobile & AI UX

Shareable principles for critique across the org. Team procedures: [AI Native Knowledge Hub](https://github.com/FirefoxUX/ai-native-knowledge-hub). Local router: `setup/agents/critique-prep.md`.

## Why critique is a system

Critique is not a show-and-tell. It exists to improve **decision quality** and **user outcomes** — not to admire artifact volume.

Good critique sessions:
- Start with a **clear decision or learning goal** (or explicitly say “explore only”)
- Anchor feedback in **principles and constraints**, not taste alone
- End with **owned actions** and a recorded outcome

Bad critique sessions:
- Walk through every screen with no ask
- Debate polish before the problem is agreed
- Produce “looks good” or vague “more exploration” with no owner

## What reviewers need from you

| Input | Minimum |
|-------|---------|
| **Problem** | Who is the user, what job, why now (2–3 sentences) |
| **Decision** | What you need from reviewers — pick one primary ask |
| **Links** | Figma (named frame), Jira key, prior decision doc if any |
| **Phase** | Discovery · Definition · Design · Validation · Handoff (see mobile+AI workflow) |
| **Constraints** | Platform, a11y, Eng scope, ship timing, brand/Nova rules if applicable |

If there is no decision ask, say **“learning goal”** instead and name what would change your direction.

## Decision types (pick one primary)

- **Direction** — which of 2–3 approaches should we pursue?
- **Scope** — MVP vs enhancement; what ships this increment?
- **Quality bar** — does this meet the bar for handoff / release?
- **Risk** — what could fail in Eng, a11y, privacy, or trust?
- **Explore** — no decision yet; feedback on problem framing or opportunity space

## Critique questions (how to write good ones)

Each question should tie to a **principle**, **constraint**, or **user outcome** — not “thoughts?”

**Strong:**
- “Does this flow preserve user agency when the AI acts on tabs? (Smart Window principle: confirm + undo)”
- “Can Eng implement states X/Y/Z from this spec without guessing? What’s missing for handoff?”
- “Does this meet WCAG focus order for keyboard users on the happy path?”

**Weak:**
- “What do you think?”
- “Any feedback?”
- “Does this feel on brand?” (without naming which brand rule)

Aim for **3–5 questions** per session. More than five usually means the packet isn’t focused.

## Time-boxed agenda (default 30 min async or 45 min live)

| Block | Time | Purpose |
|-------|------|---------|
| Context | 5 min | Problem, user, constraints, decision ask |
| Walkthrough | 15 min | Only paths relevant to the decision |
| Discussion | 15 min | Questions below; capture disagreements |
| Close | 5 min | Decision or learning; actions with owners |

## After critique

Capture in `templates/critique_notes.md` (or project `decisions.md` if scope changed):

- Decision (or “no decision — next step”)
- Slack thread link
- Actions: owner · by when · what

For Mobile + AI async reviews, follow `context-library/process/mobile_ai_design_review_workflow.md`.

## Nova / desktop chrome

If the work touches browser chrome, NTP, or settings: reviewers should check against `context-library/design-md/nova-classic/DESIGN.md` (Cursor skill: `nova-classic`).

## Red flags (agent or reviewer should call out)

- Packet is mostly deliverables with no decision or learning goal
- Spec missing states, errors, loading, or a11y for a handoff-phase review
- Scope creep disguised as “one more option” without trade-off named
- Re-litigating research in a V-B revision thread (link V-A readout instead)
