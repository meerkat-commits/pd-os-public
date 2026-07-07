# PRD Surface Map: Motion-Relevant MVP Features

Complete inventory of Smart Window MVP features and their surfaces, states,
and transitions that require motion design specifications.

Derived from: AI Mode PRDs (MVP) — 14 PRDs, 224 pages, Fx150 target.

Last updated: March 2026

## Table of Contents

1. Assistant (Core Chat)
2. Smartbar & Suggestions
3. Chat Session & History
4. Memories
5. @Mentions
6. Onboarding
7. Continuous Onboarding
8. Window Switching
9. AI Usage Metering
10. Settings
11. Multiple Model Choices
12. Smart by Default (Post-MVP)
13. Telemetry
14. Trust & Safety
15. Cross-Surface Patterns

---

## 1. Assistant (Core Chat)

**PRD author:** Jolie Huang | **Status:** Locked

### Surfaces requiring motion:
- **AI response rendering** — text streaming, markdown rendering appearance
- **Thinking/loading state** — indicator while LLM processes query
- **Search handoff** — transition from AI chat to SERP loading. Multi-stage:
  generate search query → initiate search → SERP loads → assistant responds
  based on SERP content. Can include relevant links from the SERP.
- **Follow-up question chips** — appearance below AI response, disappearance
  after selection. Follow-up is sent as user message, original chip exits
  from source response.
- **Conversation starters** — initial display on empty state (New Tab: generic
  chips like "Summarize tabs"; Sidebar: contextual per page content). Refresh
  animation needed when browsing or conversation context changes.
- **History retrieval** — transition when recalling past browsing context.
  Semantic search matches user query to high-signal history items.
- **Error states** — model unavailable, rate limit, content filtered
- **Action bar** — copy, refresh, thumbs up/down appearance below responses
- **Search suggestion links** — appearance below action bar. Mutually
  exclusive with follow-up chips. Truncated to one line, full string on hover.
  Truncate after whole word, not mid-word.

### Key states:
- Empty (new tab with conversation starters)
- User typing (smartbar active)
- AI thinking (processing indicator)
- AI responding (streaming text)
- AI complete (action bar + follow-ups OR search suggestion)
- Error (rate limit, model error, content filtered)

### Motion-critical decisions from PRD:
- "Display user sent message immediately for better perceived performance"
  (perceived latency reduction — show user message instantly, then thinking)
- Conversation starters are dynamic — refresh animation when context changes
- Search handoff is a 4+ stage process requiring distinct visual states
- Follow-up chips disappear from source response after being clicked
- Responses should have EITHER a search suggestion OR follow-up questions
  OR no actions — never both together

---

## 2. Smartbar & Suggestions

**PRD author:** Loren Austin | **Status:** Approved

### Surfaces requiring motion:
- **Smartbar focus** — gradient glow border (pink → purple) on focus
- **Placeholder carousel** (New Tab only) — continuous vertical loop of
  placeholder strings, each transitioning upward. 500ms, cubic-bezier(0.5,
  0, 0.2, 1), transform + opacity.
- **CTA button mode transitions** — the submit button changes between Ask
  (sparkle icon), Search (search icon), and Go (arrow icon) based on
  detected intent. Each mode has a different dropdown menu.
- **Suggestions dropdown** — appearance/disappearance below smartbar.
  Expands from smartbar. Shows mixed AI + search suggestions.
- **Suggestion type indicators** — sparkle (AI), search icon, globe icon
  prefix each suggestion
- **Text input → suggestion filtering** — real-time update as user types
- **Suggestion selection** — population of smartbar, routing to AI or search
- **Smartbar expansion** — vertical growth for multiline text input
- **URL detection** — mode transition to navigation mode (Go button)
- **Search engine selection** — dropdown from Search button showing Google,
  Amazon, Bing, DuckDuckGo, eBay, Perplexity, Wikipedia, Search Settings

### Key states:
- Default/empty (placeholder visible, CTA in Ask mode)
- Focused (gradient glow, placeholder carousel running)
- Typing (suggestions appear, placeholder hidden, CTA may change mode)
- Suggestion selected (routes to AI chat or search)
- URL detected (CTA transitions to Go mode)
- Multiline expanded
- Search engine dropdown open

### Responsive behavior (from Figma):
- New Tab: centered smartbar with suggestions expanding below
- Sidebar: constrained width, suggestions may overflow
- At narrow widths, suggestion text may truncate
- When suggestions reach 5+ items, responsive switch to 2-line view
- Tab title chips in sidebar context show page reference

---

## 3. Chat Session & History

**PRD author:** Jolie Huang | **Status:** Locked

### Surfaces requiring motion:
- **New Tab → chat view transition** — when user sends first message,
  the New Tab page transitions into full-width chat view. Smart Window
  logo/title area transforms into chat header.
- **Sidebar open/close** — right-side panel sliding in/out. Triggered
  by Ask button in toolbar.
- **Session persistence visual continuity** — chat persists when user
  changes pages within tab. Visual indication of continuity.
- **History list** — chat history items appearing in History view
  (accessible via bottom nav on New Tab)
- **History resume** — transition from history list to resumed conversation
- **Session reset** — clearing conversation state

### Key states:
- New tab (empty, conversation starters visible)
- Active chat — fullwidth on New Tab
- Active chat — sidebar on open tab
- Sidebar open / sidebar closed
- Replaying history (loading previous conversation)
- Session cleared

### Motion-critical from PRD:
- "Every tab has its own chat" — mental model
- Chat persists when changing pages/URLs within tab
- History is "accessible globally" — can be resumed from anywhere
- Don't show loading indicator when replaying conversation history
  (from Jira ticket)

---

## 4. Memories

**PRD author:** Jolie Huang | **Status:** Locked

### Surfaces requiring motion:
- **Memory toggle on/off per session** — from New Tab and from Sidebar.
  Timer behavior documented for the toggle transition.
- **Memory applied indicator** — when a memory is used in a response,
  visual signal. "Applied memories are visible/referenced in the
  conversation context."
- **First-time memory application** — memories used menu may auto-open
  the first time memories are applied to a response
- **Memory creation** — background process, no explicit UI animation
  for creation itself
- **Memory removal from conversation** — user can remove individual
  memories with confirmation
- **Memories Manager dashboard** (Settings) — list of all memories,
  individual delete interaction
- **Memories off via Settings** — complete disable with confirmation

### Key states (from Figma "MVP Final flows"):
- Memories on (default for session)
- Memories toggling (timer transition documented)
- Memory being applied (within response, indicator visible)
- Memory hover state (showing which memory, why it was applied)
- Memory removed (from conversation context, with confirmation)
- Memories off globally (via Settings, stops all inference)

### Post-MVP (from Figma):
- **Add memory from prompt** — user tells AI to remember something
- **Relay memory** — memory context shared across conversations

---

## 5. @Mentions

**PRD author:** Loren Austin | **Status:** Locked

### Surfaces requiring motion:
- **@ invocation** — typing @ triggers a dedicated dropdown that
  replaces the default suggestion dropdown
- **Autocomplete list** — up to 5 suggestions ranked by: open tabs →
  tab groups → recent history → free-form search
- **Entity selection** — mention chip creation in input field
- **Multiple mentions** — chip stacking behavior (limit: 5 for MVP)
- **Context chip in message** — display of referenced tabs/pages
  within sent messages and AI context

### Key states:
- @ typed (dropdown replaces default suggestions)
- Filtering (autocomplete updates as user types after @)
- Entity selected (chip created in input, dropdown closes)
- Multiple entities (chips stack in input)
- Mention limit reached (5 for MVP, configurable)

---

## 6. Onboarding

**PRD author:** Loren Austin | **Status:** Locked

### Surfaces requiring motion:
- **Sign-in flow** — account authentication transition
- **AI TOS consent** — acceptance screen. Mandated by decision log.
- **Model selection** — onboarding model picker (multiple providers)
- **Personalization setup** — background personalization begins
- **First-run introduction** — "brief, high-impact" intro
- **One-click example actions** — context-aware starter actions
- **Skip affordance** — ability to bypass steps

### Motion-critical from PRD:
- "Immediately prove AI Mode's relevance by getting users to
  successful outcomes with minimal effort"
- Background personalization begins during onboarding — no animation
  needed for background process, but transition to personalized
  experience should feel smooth
- Must be skippable — motion supports quick progression
- MVP: desktop only, English, no sync

---

## 7. Continuous Onboarding

**PRD author:** Loren Austin | **Status:** In Progress

### Surfaces requiring motion:
- **Contextual message appearance** — 3 non-disruptive messages
  anchored to browser chrome during high-signal UI moments
- **Message content** — short, contextual, action-oriented
- **One-tap affordances** — action buttons within messages
- **Message dismissal** — close/dismiss

### Key constraint:
- Must not interrupt workflow
- Anchored to browser chrome, not page content
- "Non-disruptive" is the explicit requirement

---

## 8. Window Switching

**PRD author:** Loren Austin | **Status:** In Review

### Surfaces requiring motion:
- **Window type indicator** — clear visual distinction between
  Smart Window, Classic Window, and Private Window
- **Tab drag between windows** — drag-and-drop from Smart → Classic
  or reverse
- **Mode switcher UI** — "Classic Window" (Firefox icon) / "Smart
  Window - Beta" (sparkle icon) with checkmark on active mode
- **New window creation** — opening Smart Window from Classic Mode
  (via menu: "New smart window" with Beta badge)
- **Window restoration** — state restoration after browser restart
- **"Open in smart window"** — context menu action

### Key states:
- In Classic Window (Smart Window available but not active)
- Opening Smart Window (new window creation transition)
- In Smart Window (distinct visual experience — lavender gradient)
- Dragging tab between window types
- Window restoring after restart

### From PRD:
- "Predictable state retention and restoration"
- "Clear visual indicators of window type"
- "Smooth tab/window transitions without data leakage"
- Precedent: Private Browsing window switching behavior

---

## 9. AI Usage Metering

**PRD author:** Steven Truong / Loren Austin | **Status:** In Review

### Surfaces requiring motion:
- **Usage meter** — progress toward daily cap
- **Approaching limit** — warning state
- **Limit reached** — hard stop with messaging
- **Recovery** — meter reset (daily)
- **Error messaging** — rate limit / quota exceeded states

### Key context:
- Conservative cap, easier to increase than decrease
- Primary goal: cost control without alarming users
- Calibrated through internal → alpha → public phases

---

## 10. Settings

**PRD author:** Jolie Huang / Steven Truong | **Status:** Locked

### Surfaces requiring motion (from Figma "Settings for MVP"):

**Three-level navigation architecture:**
1. **Settings > AI Controls** — Smart Window card (kill switch level).
   Smart Window appears as a card within existing AI Controls page.
2. **Smart Window sub-page** — Feature enablement, model selection,
   memory management link. States: activated (shows model picker) vs.
   not yet activated (shows setup).
3. **Memories sub-sub-page** — "Manage memories" link leads here.
   List of all memories with individual delete. Toggle for memories
   on/off. "Delete all memories" option.

### Motion surfaces:
- Navigation between settings levels (drill-in, back)
- Toggle states (memories on/off, Smart Window enable/disable)
- Model selection change (confirmation that change applies to future chats)
- Memory deletion (individual item removal from list)
- Kill switch (complete Smart Window disable)

---

## 11. Multiple Model Choices

**PRD author:** Steven Truong / Jolie Huang | **Status:** Locked

### Surfaces requiring motion:
- **Model picker in onboarding** — selection UI during first-time setup
- **Model picker in settings** — model selection with change confirmation
- **Model change confirmation** — messaging that change applies to all
  future chats (previous conversations unaffected)
- **Provider indicator** — showing which model is active (if surfaced
  in the UI)

### Key states:
- No model selected (onboarding first-time)
- Model selected and active
- Model change in progress
- Model change confirmed

### Motion-critical decisions from PRD:
- User choice and openness are guiding principles — the UI should make
  switching feel empowering, not risky
- "A description to educate users that change applies to all chats
  moving forward. Previous chats or conversations will not be altered
  or deleted."
- Multiple providers available — the picker needs to feel like a real
  choice, not a default with hidden alternatives

---

## 12. Smart by Default (Post-MVP)

**PRD author:** Loren Austin | **Status:** In Progress

### Surfaces requiring motion:
- **Default window type change** — settings toggle to make Smart Window
  the default at launch
- **Launch behavior transition** — what happens on the first launch after
  enabling Smart by Default
- **Fallback to Classic** — accessing Classic Windows when Smart is default

### Motion note:
This is post-MVP but the motion system should be designed knowing it's
coming. The default-launch experience means the New Tab page and its
initial animation (carousel, starters) becomes the *first thing every
user sees when they open Firefox*. That raises the bar significantly.

---

## 13. Telemetry

**PRD author:** (Multiple) | **Status:** Locked

### Motion relevance:
Telemetry itself has no user-facing motion surfaces, but it defines
what gets measured. Motion-relevant telemetry considerations:
- Tracking time-to-first-interaction after New Tab load (does the
  carousel help or hinder?)
- Measuring sidebar open/close frequency (does the animation speed
  affect usage?)
- Conversation starter click rates (does their appearance animation
  affect discoverability?)
- Follow-up chip usage (does the disappear/reappear choreography
  cause confusion?)

### Why this matters for motion design:
Every motion decision should be measurable. When defining motion specs,
include what telemetry events should fire to validate that the motion
is serving its purpose. Example: if the thinking state animation is
designed to communicate "AI is processing," telemetry should track
whether users wait patiently or repeatedly re-submit queries.

---

## 14. Trust & Safety

**PRD author:** (Team) | **Status:** Locked

### Surfaces requiring motion:
- **Content filtered response** — what the user sees when the AI's
  response is blocked for safety reasons
- **Sensitive info detection** — indicator when the system detects
  potentially sensitive content in the query
- **Error states from content filtering** — distinct from model errors
  or rate limits

### Motion-critical decisions:
- Filtered/blocked responses should feel firm but not alarming
- The motion should clearly distinguish "I can't answer that" (content
  filter) from "something went wrong" (error) from "you've used too
  much" (rate limit)
- Trust & safety states should never use the same animation as the
  normal thinking state — the user should immediately know this is
  a different kind of response

---

## 15. Cross-Surface Patterns

These motion patterns recur across multiple PRD surfaces and need
consistent treatment system-wide:

### AI Thinking State
**Appears in:** Assistant, Suggestions (AI-generated), @Mentions
(semantic search), Search handoff (generating query)
**Needs:** A single, recognizable "AI is processing" pattern that can
show different stages when the process has stages.

### Text Streaming
**Appears in:** Assistant responses, search handoff synthesis
**Needs:** Consistent text appearance — word-by-word, line-by-line,
or block-by-block. Must feel responsive without being artificially
delayed.

### Panel/Surface Transitions
**Appears in:** Sidebar open/close, New Tab → chat view, Settings
navigation, Onboarding flow, Window switching
**Needs:** Consistent spatial animation language with clear origin
and destination.

### Chip/Pill Creation and Removal
**Appears in:** @Mentions chips, follow-up question chips, conversation
starter chips, quick action chips, context chips
**Needs:** Consistent enter/exit behavior. Special case: follow-up
chips that exit source and become user messages.

### List Item Management
**Appears in:** Memories Manager, Chat History, Suggestions dropdown,
@Mentions autocomplete
**Needs:** Consistent list item enter/exit/reorder/delete behavior.

### Toggle/Switch States
**Appears in:** Memories toggle (per session), Settings toggles, Model
selection
**Needs:** Consistent state change feedback.

### Error and Limit States
**Appears in:** Rate limiting, model errors, content filtering, network
issues, quota exceeded
**Needs:** Consistent error appearance that communicates clearly without
alarming.

### Empty States → Active States
**Appears in:** New Tab → first chat, empty sidebar → active
conversation, first-time → configured (onboarding)
**Needs:** Consistent "awakening" transition from empty/waiting to
populated/active.

### Button Mode Transitions
**Appears in:** Smart bar CTA (Ask → Search → Go), Ask button in
toolbar (chat closed → chat opened)
**Needs:** Smooth state transitions as detected intent changes.
