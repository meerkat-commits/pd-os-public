# PD-OS weekly agent

Run after `run-weekly` completes (or read the latest rollup yourself).

## Goal

Synthesize the prior calendar week: commitments, concerns, and patterns across people.

## Read first

1. Latest file in `data/rollups/weekly/` (`YYYY-MM-DD__to__YYYY-MM-DD.md`).
2. Skim `data/people/` only when you need context on a specific relationship.

## Output

1. **Week in one paragraph** — what dominated meetings and decisions.
2. **Commitments ledger** — grouped by person; flag anything stale or duplicated.
3. **Concerns / pushback themes** — patterns, not every quote.
4. **Carry into next week** — max 5 priorities for design leadership focus.

## Constraints

- Decision hygiene: note what was decided vs still open.
- Don’t merge or rewrite person files; append-only repo convention applies to humans too.
