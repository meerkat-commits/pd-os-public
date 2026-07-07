# Smart Window Design System

Reference for the Smart Window (AI Mode) visual language, components, and
interaction patterns. This document is derived from the current Figma specs
and should be used when prototyping or documenting components.

Last updated from design screenshots: March 2026

## Table of Contents

1. Visual Identity
2. Core Surfaces
3. Components
4. Interaction Patterns
5. Responsive Behavior
6. Theme Support

---

## 1. Visual Identity

### Brand Mark
- **Smart Window** logotype paired with a four-pointed star icon
- Star icon uses a gradient: orange-red to pink-purple (warm to cool)
- "Smart Window" text in a medium-weight sans-serif, purple tone
- "Beta" badge appears as a small pill tag next to the title during beta period

### Color Palette (Light Theme — Primary)
- **Background:** Warm lavender-pink gradient (very light, ~#F5EEFF to #FDEEF5)
- **Primary accent:** Purple (#7B5EA7 range) — used for active states, icons, borders
- **Secondary accent:** Orange-red to pink gradient — star icon, active CTA buttons
- **Surface:** White with subtle border (#FFFFFF, border ~#E8E0F0)
- **Text primary:** Dark charcoal/near-black
- **Text secondary:** Medium gray
- **Chip/pill borders:** Light purple-gray (#D8D0E8 range)
- **Bottom nav icons:** Purple outline style when active, gray when inactive

### Color Palette (Dark Theme)
- **Background:** Deep navy/dark purple
- **Surfaces:** Dark elevated cards with subtle purple borders
- **Text:** White primary, light gray secondary
- **Accent colors:** Same gradient star icon, orange/red CTAs carry through
- **The Ask button in toolbar:** Orange-red fill with white text in dark theme

### Typography (observed)
- Headings: Sans-serif, medium-to-bold weight (likely Firefox system font / Inter)
- Body text in chat responses: Supports full markdown rendering (H1-H3, bold,
  italic, links, lists, code blocks, blockquotes)
- Placeholder text: Light gray, regular weight
- Bottom nav labels: Small, regular weight

---

## 2. Core Surfaces

### New Tab Page (Smart Window Home)
The primary landing surface when opening a new tab in Smart Window mode.

**Layout (vertically centered on page):**
- Smart Window logo + title (centered)
- Smartbar input field (centered, ~60% page width)
- Quick action chips row (centered, below input)
- Bottom navigation bar (fixed to bottom)

**Key behaviors:**
- New Tab does NOT display toolbar controls in a fresh instance
- If user navigates to a website then navigates "back," New Tab shows toolbar
  controls minus the address bar
- Works with horizontal tabs, horizontal tabs + bookmarks visible, and
  vertical tabs + bookmarks visible configurations

### Sidebar Panel
The Smart Window chat interface that overlays on top of browsing content.

**Layout:**
- Appears as a right-side panel overlaying the current page
- Contains: chat messages, smartbar input at bottom
- Narrower than full New Tab — constrained panel width
- Placeholder string in sidebar: "Ask anything..."
- Unlike New Tab, sidebar does NOT have rotating placeholder animation
- Smart bar is in focus state, continuing from an AI/User's current conversation

### Chat Response Area
Where AI responses render within either New Tab or sidebar contexts.

**Content rendering:**
- Full markdown support: headings, bold, italic, links, lists, code
- Spacing and styles documented across heading levels
- Tested across multiple themes (light, dark, warm variants)
- Link text appears in accent color (orange-red)
- Response formatting maintains readable line lengths

---

## 3. Components

### Smartbar (Unified Input)

The primary input surface — serves as ask, search, and URL entry combined.

**Anatomy:**
- Multi-line text input area (top portion)
- Placeholder text: rotating carousel in New Tab, static in sidebar
- Bottom row: attachment button (+), image/camera button, spacer, submit arrow (→)
- Subtle rounded-rectangle container with light border
- Gradient glow/border treatment on focus (pink-to-purple outer glow)

**States (light theme):**
- Default/empty: Placeholder text visible, subtle border
- Focused: Gradient glow border appears (pink → purple)
- With text entered: Text replaces placeholder
- With multiline text: Input expands vertically
- URL detected: Transitions to navigation mode
- Focused + results/empty: Displays content below in dropdown

**States (dark theme):**
- Same states as light but on dark surface
- Border glow is more prominent against dark background
- Orange/red submit button more visible

**Placeholder Carousel (New Tab only):**
- Continuous vertical loop of placeholder strings
- Strings rotate with delay between cycles
- Each string stacks vertically and transitions upward, one at a time
- Transition reveals next string as current one disappears upward
- Initial string visible when New Tab opens, no fade-in delay

Placeholder strings (in order):
1. "Ask, search, or type a URL"
2. "Ask AI to research recent finds..."
3. "Enter a web address..."
4. "Search the web..."
(Additional strings may rotate)

Animation specs:
- Duration: 500ms
- Easing: cubic-bezier(0.5, 0, 0.2, 1)
- Property: transform + opacity

**Sidebar variant:**
- Single static placeholder: "Ask anything..."
- Placeholder disappears when user starts typing
- Smart bar is in focus, continuing from conversation context

### Quick Action Chips

Row of suggested actions below the Smartbar on New Tab.

**Current chips:**
- "Summarize tabs"
- "Improve writing"
- "Compare tabs"

**Styling:**
- Pill-shaped with light border (purple-gray)
- Text in regular weight, dark color
- No fill — ghost/outline style
- Horizontal row, centered, small gap between
- Subtle hover state (likely light fill)

### Ask Button (Toolbar)

Entry point to Smart Window from Classic Mode browsing.

**Placement:** Right side of browser toolbar, after other toolbar buttons

**States (light theme):**
- Chat closed, default: Orange-red pill with "Ask" text + sparkle icon
- Chat closed, hover: Slightly different treatment (v1)
- Chat opened, default: "Ask" text + arrow icon (no fill, outline style)
- Chat opened, hover: Subtle highlight

**States (dark theme):**
- Chat closed, default: Orange-red fill, white "Ask" text + sparkle icon
- Chat closed, hover: Brighter/emphasized
- Chat opened, default: Outline style "Ask" with arrow
- Chat opened, hover: Subtle highlight

**Also appears as:** "Search" pill button (orange-red gradient) in some contexts

### Beta Badge

**Inline with title:** Small "Beta" text badge next to "Smart Window" title

**In menus:**
- "New smart window" menu item shows "Beta" pill badge (outlined)
- Window mode switcher: "Classic Window" (Firefox icon) / "Smart Window - Beta"
  (sparkle icon) with checkmark on active mode

### Bottom Navigation Bar

Fixed to bottom of New Tab page.

**Items:**
- History (clock icon)
- Chats (chat bubble icon)
- Settings (gear/cog icon)

**Styling:**
- Icon + label pairs, evenly spaced
- Purple outline icons
- Text labels below icons, small size
- No visible background bar — floats on the gradient background

**Note:** In some screens, Settings is not visible (only History + Chats).
This may be a viewport or variant difference.

### Suggestions Dropdown

Appears below the Smartbar when user begins typing.

**Behavior:**
- Triggered on input, expanding from the Smartbar
- Shows suggested queries with different sources indicated
- Entries prefixed with icons indicating type:
  - Sparkle icon: AI-suggested queries
  - Search icon: Default search engine suggestions
  - Globe icon: URL/site suggestions
- Shows up to ~6 suggestions initially
- Typing filters/updates suggestions in real-time

**Ordering logic (from spec):**
- SEARCH: Search (default search engine suggestion)
- KEYWORD: Keyword search
- AI_QA: AI quick answer suggestion
- AI_TA: AI tab-aware suggestion
- AI_PA: AI page-aware suggestion

**Rules from spec:**
- If typed text contains terms that match suggestions, show 4-8 options
- Mix of AI-generated and traditional search suggestions
- Show brief blue link for AI sources when applicable
- If suggestions overflow the field, length of the suggestions row is 4 options
- Max of 4 buttons overflow, input text also overflows below the field
- Input text also stays in place after clicking

**Interaction on selection:**
- Selecting a suggestion populates the Smartbar
- May trigger search (navigates to SERP) or AI response (stays in Smart Window)
- Sparkle-prefixed suggestions route to AI; search-prefixed route to search engine

---

## 4. Interaction Patterns

### Flow A: Suggested Search in Conversations

**From New Tab:**
1. User lands on Smart Window New Tab
2. Types query in Smartbar (e.g., "best 3D printers")
3. Suggestions dropdown appears with mixed AI + search suggestions
4. If user selects search suggestion → navigates to Google SERP
5. SERP loads within Smart Window tab
6. Smart Window can offer follow-up context on the search results

**From Sidebar:**
1. User is on a website (e.g., Booking.com hotel listing)
2. Opens Smart Window via Ask button in toolbar
3. Sidebar appears with contextual suggestions based on current page
4. User can ask questions about the page content
5. AI responds with page-aware answers in the sidebar
6. Conversation continues in sidebar alongside the web page

### Flow B: Send Prompt After 1:1 SERP

1. User starts in Smart Window New Tab
2. Types query → sees suggestions → selects search
3. Navigates to Google SERP within Smart Window
4. After viewing SERP results, user can "auto-send query" to Smart Window AI
5. AI provides synthesized answer based on search results
6. Can include rich content: images, product cards, links
7. Follow-up conversation continues from that context

### Flow C: Manual Search Handoff

1. User starts in Smart Window New Tab
2. Types query → suggestions appear
3. Selects a traditional search result
4. SERP loads, user browses through results normally
5. User can manually invoke Smart Window AI via sidebar at any point
6. AI provides assistance based on current browsing context

### Responsive Behavior

The Smart Window interface adapts across window widths:

**Narrow width (sidebar-like):**
- Smartbar and suggestions stack vertically
- AI responses constrain to panel width
- Quick action chips may wrap

**Medium width:**
- Standard layout with centered Smartbar
- Suggestions dropdown below

**Full width (on website with sidebar):**
- Sidebar panel overlays right side of page
- Page content shifts or is partially covered
- Sidebar has its own scrollable area

**Width handling for suggestions on websites:**
- Suggestions overlay can extend beyond the sidebar if needed
- Or constrain to sidebar width with scrollable overflow

---

## 5. Responsive Behavior

### Window Configurations Tested
- Horizontal tabs (default)
- Horizontal tabs + bookmarks bar visible
- Vertical tabs + bookmarks visible

### Breakpoint Notes
- New Tab layout remains centered at all tested widths
- Sidebar panel appears to have a min-width constraint
- On narrower viewports, suggestion text may truncate
- "Set this as your URL" tooltip appears when the AI detects a URL-like entry
  that could set up the browser to visit a specific page

---

## 6. Theme Support

### Confirmed Themes
- **Light (default):** Lavender-pink gradient background, white surfaces
- **Dark:** Deep navy/purple background, dark elevated surfaces
- **Warm variant:** Peach/amber tones (visible in text formatting examples)

### Theme Application
- All components have been tested across light and dark themes
- Chat response formatting (markdown) renders correctly in all themes
- Smartbar states documented for both light and dark
- Ask button has explicit light and dark variants

### Theme-Specific Notes
- Gradient glow on Smartbar focus is more visible in dark theme
- Orange-red accent colors provide stronger contrast in dark theme
- Link colors in chat responses adjust per theme
- Background gradient shifts warmth/coolness per theme

---

## 7. MVP Flows & Interaction Specs

### Core Flow (MVP)
The primary end-to-end flow for Smart Window MVP:
1. User opens Smart Window (New Tab or via Ask button)
2. Types query in Smartbar
3. AI responds in full-width chat (New Tab) or sidebar panel (open tab)
4. Conversation continues with follow-ups
5. User can navigate to search results or websites from within the conversation
6. Memory system tracks context across sessions (when enabled)

### Conversation Starters

**From New Tab:**
- Quick action chips ("Summarize tabs," "Improve writing," "Compare tabs")
  appear below the Smartbar
- Selecting a conversation starter auto-sends it into full-width chat
- The LLM responds with clarifying questions (e.g., "Compare tabs" → "I can
  help with that! Please tell me which tabs you would like me to compare...")
- The New Tab page transitions into the chat view after sending

**From Open Tab (Sidebar):**
- Conversation starters appear as contextual buttons in the sidebar
  based on the current page content
- Example on TripAdvisor: "Summarize the tour highlights" /
  "Compare this to others"
- Selecting a conversation starter sends it as a user message
- AI responds with page-aware content in the sidebar

### Follow-up Questions

- Follow-up questions are nested within the triggered response
- They appear as clickable suggestion chips below the AI response
- Upon selecting a follow-up action, it is sent as a user message
- The original follow-up button disappears from the source response
  after being clicked
- Follow-ups maintain conversational context from the original query
- Example flow: "Summarize the tour highlights" → AI responds →
  "Do they pick up from downtown hotels?" → AI responds with
  page-specific answer → "Check for my hotel" → AI provides
  location-specific details

### Search Suggestions (Suggested Search Links)

**When they appear:**
- Search suggestions appear when the assistant can answer from its own
  knowledge, but a search could provide additional or more current information

**Key rules:**
- Search suggestions should NOT appear alongside follow-up questions
  (this avoids users asking more questions on a topic where the model
  has already flagged its own limitations)
- Responses should have EITHER a search suggestion OR follow-up questions
  OR no actions — never both together

**Visual treatment:**
- Search suggestions reuse the same styling as "Search results" links
  (the search handoff pattern)
- Logo of the default search engine is shown with the link
- Search suggestion strings should be truncated to one line spanning
  the width of the assistant text area
- The full string can be accessed on hover
- Truncation rule: If possible, truncate after a whole word, not mid-word
  (e.g., "Search 'why is the sky blue on Earth...'" not
  "Search 'why is the sky blue on Earth com...'")

**Action bar below responses:**
- Copy, Refresh, Thumbs up/down icons appear below AI responses
- Search suggestion appears as a separate linked element below the
  action bar

---

## 8. Memory System (MVP)

### Overview
Smart Window includes a memory system that learns from conversations to
provide more personalized responses over time.

### Toggling Memories Per Session

**From New Tab:**
- Memory toggle available in the conversation context
- User can turn memories on/off for the current session

**From Sidebar:**
- Same toggle behavior available within sidebar conversations

### Memories Applied
- When memories are active, the AI uses stored context to personalize
  responses (e.g., remembering product preferences, past research topics)
- Applied memories are visible/referenced in the conversation context

### Removing a Memory
- Users can remove individual memories from the conversation context
- Removal flow shown with confirmation steps

### Memories Off via Settings
- Memory functionality can be completely disabled through Settings
- When memories are toggled off at the settings level, conversations
  don't store or reference any memory data
- "Memories" toggle + clear toggle states documented
- Turning memories back on requires explicit user action

### Toggle Timer Behavior
- When toggling memories on/off, there's a transition behavior
  documented for both New Tab and sidebar contexts

### Post-MVP Memory Features
- **Add memory from prompt:** Users can explicitly tell the AI to remember
  something from within a conversation
- **Relay memory:** Memory context can be shared/relayed across different
  conversation contexts

---

## 9. Settings Architecture (MVP)

### "Smart Window" Card on AI Controls (Kill Switch)
- Smart Window appears as a card within Firefox's existing AI Controls
  settings page
- This is the top-level entry point — a kill switch that can disable
  Smart Window entirely
- The card integrates with the existing "Block AI enhancements" toggle
  pattern from Firefox 148
- Smart Window settings sit alongside other AI feature controls
  (translations, tab groups, link previews, chatbot, etc.)

### "Smart Window" Sub-Page
- Clicking into the Smart Window card opens a dedicated sub-page
- Contains Smart Window-specific settings:
  - Feature enablement
  - Model selection (choice of AI model — key Firefox differentiator)
  - Memory management link
  - Other Smart Window-specific preferences
- States documented: Smart Window activated (card shows model picker),
  Smart Window not yet activated (shows setup flow)
- Model picker shows available models (multiple providers)

### Memories Sub-Sub-Page
- Accessible from the Smart Window sub-page via "Manage memories" link
- Dedicated page for viewing and managing all stored memories
- Shows list of memories with ability to delete individual items
- Memories are presented as readable descriptions of stored context
- Page lists all memories that route is collecting

### Settings Navigation Path
Settings → AI Controls → Smart Window (card) → Smart Window (sub-page) →
Manage Memories (sub-sub-page)

