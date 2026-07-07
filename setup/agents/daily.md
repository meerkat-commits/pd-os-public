# PD-OS daily agent

Run after `run-daily` completes (or read the latest digest yourself).

## Goal

Turn today’s PD-OS digest into a short leadership brief: what changed, who owes what, and what needs a nudge.

## Read first

1. Latest file in `data/digests/` (today’s date).
2. If a section is `_None found_`, say so briefly — don’t invent items.

## Output (keep under ~15 bullets)

1. **Top themes** (3–5 bullets) from Meeting context.
2. **Commitments to track** — person, meeting, one-line ask.
3. **Pushback / risks** — person, concern, suggested follow-up.
4. **Preference signals** — only if useful for how to frame messages this week.
5. **Suggested actions** — max 3 concrete next steps for Brook.

## Constraints

- Narrative over artifact volume.
- Don’t overwrite `data/people/` history; this is a read-and-synthesize pass.
- Link to person files under `data/people/` when naming someone repeatedly.
