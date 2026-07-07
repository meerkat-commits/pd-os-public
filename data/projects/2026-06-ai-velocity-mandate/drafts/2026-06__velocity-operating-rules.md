# Velocity operating rules

**One-pager** — how we run the three bets without gaming proof.  
*Input: Eduardo Feo · 2026-06-23 · Priority update: Brooke · 2026-06-23*

**Sequencing:** QA and papercuts **now**. Faster calls **ongoing**. Code in the Firefox tree is a **stretch** target, not the default bar for every designer.

---

## Bet 1 — QA & close the loop (now)

**Single backlog for visual gaps** — punch findings must not fragment across Jira + GitHub with no owner. One queue, one DRI to close the loop.

### Punch severity (Nova builds now)

| Level | Meaning |
|-------|---------|
| **Blocker** | Must fix before wider exposure |
| **Fix before exposure** | Should fix; don’t ship as-is |
| **Accept and track** | Known gap — log it and move on |

### Papercuts (post-Nova Nightly, ~post-July)

User-visible polish and small UX fixes shipped from one queue — same backlog discipline as punch. Leadership aligned on timing.

**Monthly proof:** gaps opened/closed from the single queue; punch issues caught before wider exposure.

---

## Bet 2 — Faster calls: tactical vs strategic (ongoing)

| | **Tactical** → fast call | **Strategic** → deep qual |
|---|--------------------------|---------------------------|
| **What** | Reversible UI/flow choice; single segment; answerable in &lt;48h | Big bet; trust/privacy/new-user risk; needs segments |
| **Method** | AI-moderated / UserTesting-style fast signal (rounded-corners fast-signal model) | Full qual — not a quick test |
| **Proof bar** | Fast signal **changed** a decision — not “we ran a test” | Documented why fast signal was insufficient |

**Monthly proof includes at least one case** where fast signal changed the call (decision **quality**, not just decision speed).

---

## Bet 3 — Code, not slides (stretch)

For designers already shipping in the Firefox tree (Jeff, Nicole, Eduardo patterns). **Not required of everyone in H1.**

| Tier | Bar | Proof |
|------|-----|-------|
| **Eng-used** | Prototype linked in **sprint planning** or eng ticket | Bug/task: “Implement per prototype in [link]” |
| **Exploratory** | Local HTML/Loom for alignment — valuable, not counted alone | — |

Designers initiate in code when it unblocks Eng; partners co-create — not QC for Cloud mocks.

---

## What we won’t count as proof

Avoids credibility loss when month 2 looks like motion without impact:

- Loom or local HTML with **no eng ticket / sprint link** (especially as a substitute for QA closure)
- “We ran a test” with **no decision change**
- Punch findings filed in **three places** with no closure
- Claiming code-native velocity when the win was a **papercut or spec fix**
- Velocity theater (more files, same shipped outcomes)

---

## Pillar owners

Eduardo · Emanuela · Nicole — coach visibility + in-progress sharing; not new rituals from Brooke.
