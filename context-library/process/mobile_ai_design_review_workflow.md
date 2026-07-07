## Mobile + AI — async design review workflow

Align with your org's async design review playbook (phase prefixes, Slack + Jira spine).

### Principles

- **Slack**: conversation + visibility; threads carry the review; use your team's design-review channel
- **Jira**: durable scope, decisions, handoff, links back to Figma and Slack
- **Explicit triggers**: post when work is ready for a phase exit, not on every edit
- **Incremental delivery**: right-size fidelity/ceremony to the increment

### Delivery phases (paths)

- **Discovery**: understand space → problem statement / prioritized opportunity
- **Definition**: align on approach → scoped solution (MVP vs enhancement)
- **Design**: develop solution → build-ready design (right-sized)
- **Validation**: test/refine → confidence appropriate to release risk
- **Handoff**: specs + alignment → team ready to execute increment
- **Build support**: implementation/quality → increment shipped
- **Post-launch**: outcomes/learnings → inputs for next iteration

### Slack post template

```text
Channel: #your-design-review-channel
[Mobile+AI · <Phase>] <short title>
Owner: @…
Jira: <EPIC- or KEY-123>
Figma: <link> (frame: <name> or “n/a”)
Exit we’re aiming for: <one line from the phase list above>
What we need: …
By when: …
Thread = review.
```

### Jira spine

- Anchor work on an **Epic** (or parent story) per increment
- Every Slack review post links the **same Jira key**
- Decisions that change build scope belong in Jira (comment / acceptance criteria), not only Slack

### Validation (V-A / V-B)

- **V-A — study readout**: findings ready for decisions (Research owns artifact)
- **V-B — design revision**: UI changes mapped to findings (Design owns frames; link the V-A readout)

Rule: in V-B threads, don’t re-litigate the study; link back to V-A.

### Heuristics plugin (signal, not a gate)

Heuristic checks can be a useful pre-flight before posting `[Mobile+AI · Design]`, but completion is a **signal** (someone ran a pass), not proof the phase exit is met.

### PD-OS hooks

- **Heuristic pre-flight (optional)**: **`setup/agents/heuristics-review.md`** — same lenses as the Heuristics Figma plugin (`design/heuristics-plugin/`)
- **Before review**: run **`setup/agents/critique-prep.md`** (or `context-library/process/critique-prep.md` for principles only)
- **Discovery/Definition**: `templates/design_brief.md` + a project folder under `data/projects/<initiative>/brief.md`
- **Design**: capture async review outcomes using `templates/critique_notes.md` and link the Slack thread in the project `drafts/` or `decisions.md`
- **Validation**: store readouts in `data/projects/<initiative>/research/` and map findings → frames
- **Handoff**: record decisions in `decisions.md` and mirror acceptance criteria into Jira

