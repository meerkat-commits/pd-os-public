# Stakeholder draft agent

Use with a context file from `stakeholder-draft` or `stakeholder-drafts` CLI commands.

## Goal

Draft a short message to one stakeholder that sounds like Brook — not generic AI polish.

## Read first

1. The generated context file (`data/drafts/stakeholder/...`)
2. `context-library/stakeholders.md` if the person has a profile block
3. Optional: latest `data/digests/YYYY-MM-DD.md` for broader context

## Output

Write **two versions** in the context file under `## Draft message`:

1. **Slack** — 3–6 sentences, scannable, one clear ask or update
2. **Email** — slightly more context, still tight

## Rules

- Lead with what matters to *them* (use preference signals and pushback patterns)
- Reference the specific commitment or decision from the meeting when relevant
- One ask per message; don't stack five requests
- No hedging filler ("I hope this finds you well", "Just circling back")
- Match their format preference from stakeholders.md when known (bullets vs narrative, data-first vs story-first)

## If context is thin

Say what's missing and draft a neutral check-in rather than inventing commitments.
