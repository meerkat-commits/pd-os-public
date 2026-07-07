# Product Context: Firefox AI Strategy

This reference contains the full internal product context for the Firefox AI
strategy, synthesized from internal strategy documents, the strategy deck, and
public announcements. Read this when you need grounding in the product before
producing any output.

## Table of Contents

1. Strategic Vision & Hypothesis
2. Three Browsing Modes
3. Target Personas
4. Problem Priorities
5. Technical Architecture
6. Competitive Landscape
7. Revenue Context
8. Shipped Features & Roadmap
9. AI Mode Concepts
10. Investment Scenarios
11. Key Stakeholders & Teams
12. Design Constraints & Guardrails

---

## 1. Strategic Vision & Hypothesis

**Vision:** Firefox's mission is to make powerful AI accessible to everyone.
"Your Private AI sidekick for a smarter, friendlier web where you can get
things done faster."

**Framing:** Powerful AI + Uncompromising Privacy = Your Digital Life,
Supercharged.

**Hypothesis:** Users who use Firefox's privacy-preserving AI find more value,
retain better, engage more, and are more satisfied. This proves that
privacy-focused intelligent browsing influences user loyalty and browser choice.

**Strategic approach:**
- Move fast: Show users Firefox is innovating with responsible AI
- Reusable AI capabilities: Build capabilities reusable across Firefox/Mozilla
- Legal awareness: Acknowledge AI legal risk, leverage small relative exposure
- Open-source models + selective integration: Don't build foundational models
- Local-first + hybrid: Prioritize on-device, cloud fallback with consent
- Breadth-first for 2025: Ship simple high-value features to find what resonates
- Mobile-first growth: Lean into mobile where Firefox is gaining traction

**Expected outcomes:**
- Scale AI weekly active users 20x to 1M in 12 months
- Deliver 4-5 highly adopted AI features by end of 2025
- Improve retention among Gen Z and AI-adopting users
- Strengthen Firefox's brand as most trusted AI-era browser

**Strategy driver:** Tapan Kamdar (approved May 28, 2025)

---

## 2. Three Browsing Modes

Firefox builds for the full AI adoption bell curve — not picking one path.

### Private Mode
For users who want the most private default AI settings. On-device processing
only. No cloud. Maximum privacy. Maps primarily to Josef's needs.

### Classic Mode
The familiar Firefox with intelligent support. AI offers light-touch support
that enhances flow without interrupting it. Provides helpful suggestions
without using browsing context. Runs on-device. Easy to ignore, dismiss, or
refine. This is the default experience for most users.

### AI Mode (AI Window / Smart Window)
The most intelligent, personalized experience. A new opt-in browsing mode
alongside Classic and Private. Turns Firefox into a private, context-aware
assistant. Key characteristics:
- Uses browsing context to deliver personalized support
- Coordinates specialized agents to complete complex tasks
- Gives full control over what's remembered
- Proactively moves tasks forward without getting in the way
- Designed to compete head-on with challengers like Dia

The strategy deck positions AI Mode as the response to AI-first browsers,
while Classic Mode improvements address the AI-augmented browser category.

---

## 3. Target Personas

### Josef — "Build trust with him"
- Privacy-conscious tech enthusiast
- Gen X, traditionalist, desktop-first
- Values control, clarity, security, reliability, efficiency
- Views new tech through a critical lens: curious but cautious
- Most receptive to AI that clearly enhances everyday productivity
- Discovery features only compelling if highly configurable and optional
- Engages with automation when he can opt in on his terms
- "Trust is the foundation; intelligence is a bonus"
- Everyday Productivity: Strong
- Smart Discovery: Limited
- Power Users & Automation: Strong

### Mina — "Design for her"
- Practical, values-driven multitasker
- Millennial, organized, prefers mobile
- Life is busy, mobile-centered, overloaded with digital clutter
- Drawn to solutions that reduce friction and help stay organized
- Values AI that quietly enhances workflow without demanding input
- Appreciates personalized guidance only when thoughtful, not feed-like
- Smooth intuitive experience more valuable than power or complexity
- Everyday Productivity: Strong
- Smart Discovery: Strong
- Power Users & Automation: Low

### Avery — "Market to her"
- Next-gen independent thinker
- Gen Z, mobile-first, wants to focus
- Mobile-native creator and explorer, constantly switching contexts
- Expects technology to adapt to her, not the other way around
- Responds strongly to dynamic, deeply personalized themes
- Excited by AI that feels interactive and fun, not rigid
- Automation resonates when it supports independence
- Everyday Productivity: Strong
- Smart Discovery: Very Strong
- Power Users & Automation: Selective

---

## 4. Problem Priorities

### Priority 1: Everyday Productivity (Foundation)
The base layer. Simple, high-frequency tasks that resonate broadly.

- **Effortless Content Consumption:** Summarize web pages, PDFs, video transcripts
- **AI Summaries:** Mobile-native gestures (pinch, shake) for instant summaries
- **Digital Memory Recall:** Resurface the right page/insight from history
- **Contextual Writing Companion:** Draft emails/posts in your tone from page content
- **Quick Natural Search:** Voice/image inputs, location-based suggestions
- **Personalized Focus Space:** Calendar integration, deep work suggestions
- **Cross-Device Continuity:** Start on mobile, continue on desktop with context
- **In-Browser Learning Coach:** Surface key concepts, real-time explanations
- **Contextual Page Q&A:** Reimagined Ctrl+F with natural language questions

### Priority 2: Smart Discovery & Engagement
Deepen engagement through intelligent discovery and personalization.

- **Answer Bar:** Address bar as thought partner + answer engine + discovery assistant
- **Adaptive Content Recommendations:** Suggest articles/videos aligned to interests
- **Context-Specific Feeds:** Dynamic new tab based on work, location, topics
- **Personalized Learning:** Curate reads, generate multimedia learning content
- **Content Transformation:** Convert content to preferred formats (audio dialogues)

### Priority 3: Power Users & Automation
Advanced capabilities for workflow automation and deep information interaction.

- **Automated Multi-Step Planning:** Orchestrate trips, scheduling, etc.
- **Agentic Automation:** Resume collection, cover letter generation, etc.
- **Consolidated Information Aggregation:** Multi-source unified view
- **Complex Content Analysis:** Browser as MCP client, cross-reference local + web

### Problems on the Horizon (Future Considerations)
- Fragmented AI workspace (users adopt multiple AI tools/agents)
- Unclear boundaries between local and cloud AI
- AI task continuity and memory across sessions and devices
- Loss of agency in autopilot AI environments
- Agent overlap and conflicting guidance

---

## 5. Technical Architecture

### Hybrid AI Stack
**Local on-device:**
- Inference runtime: Transformers.js, ONNX, WASM
- C++ bindings for performance optimization
- Web Extension inference engine (flexible API for developers)
- Inferred personalization using differential privacy (local data only)
- On-device learning from browsing data
- LoRA adapters: Single large model + specialized small adapters per task
- Models under exploration: Gemma, Gemini Nano, AI2 OLMo, Phi-4

**Cloud-hosted:**
- Mozilla-hosted foundational model on GCP or Azure
- Only with explicit user consent
- Prompt-based usage for minimal data transfer
- Partners: Vertex AI (ongoing), Together.ai, Groq (exploration)
- Anthropic, OpenAI also under exploration for cloud inference

**AI Tooling:**
- Hugging Face, ONNX Runtime (ongoing)
- Flower.AI (exploration)

**Cross-platform frontend (XPFE):**
Firefox's unique advantage — desktop apps built with HTML/JS/CSS on Gecko,
deployed at scale across Windows, Mac, Linux. Enables vertical solutions,
customization, and rapid prototyping. Other browsers have different native
frontends per OS.

### Agentic Browsing Strategy
- Browser as "brain" (MCP client), not "appendage" (MCP server)
- Focus on solving practical UX problems (prompt injection, messy UX)
- Select a few agentic features and iterate, not generic "prompt to actions"
- Collaborating with innovation team (TABS) on web extension-based tools
- Testing with swappable models (API-based and local open source)
- Evaluating MCP role: could use MCP ecosystem to connect third-party
  functionality that doesn't map to web extensions

---

## 6. Competitive Landscape

### AI-Augmented Browsers
- **Chrome (Gemini):** Massive user base, deep ecosystem, weaving in generative
  AI for search. Trust issues from data collection.
- **Edge (Copilot):** Microsoft Copilot deeply embedded across browser and OS.
  Enterprise productivity focus. Less privacy-conscious.

### AI-First Browsers
- **Dia (The Browser Company):** Tab-aware assistant, personalized memory,
  encrypted local context. Primary competitive threat for AI Mode.
- **Comet (Perplexity):** Research-focused, LLM-native browser with
  citation-backed insights. Building its own privacy-light browser.

### Agentic AI Browsers
- **Opera Neon / Opera GX:** AI chat, code/content generation, paid premium
  "Chat, Do, Make" tools.
- **OpenAI Operator:** Built to use its own browser to do things on user's
  behalf from within chat.

### Other Threats
- Apple Safari: Hybrid approach (Apple Intelligence + ChatGPT), limited to
  Apple ecosystem
- Brave, Arc, Vivaldi: Smaller browsers experimenting with AI, burning VC
- AI companies building browsers (OpenAI + Yahoo pitched to buy Chrome,
  Perplexity's Comet) — browsers seen as critical access to user behavior

### Firefox's Competitive Differentiation
What makes Firefox unique in this landscape:
- Local + Cloud approach with privacy-preserving AI
- User choice of AI model (not locked to one ecosystem)
- Mozilla's trusted legacy of openness, user choice, data transparency
- Open-source heritage and community-driven innovation
- Cross-platform frontend enabling rapid iteration

---

## 7. Revenue Context

AI is expected to have increasing negative revenue impacts on Firefox's
search-based business model:

| Year | Revenue Impact from AI |
|------|----------------------|
| 2025 | $0M                  |
| 2026 | -$16.4M              |
| 2027 | -$28.4M              |
| 2028 | -$40.1M              |

- Non-revenue generating search volume declining ~6.5% YoY
- Revenue generating search volume declining ~2.3% YoY
- Ad click rate declining ~2%
- Total search volume estimated to fall by 2.2B by 2028

This creates urgency: Firefox must deliver differentiated AI value to
retain users and find new engagement/monetization models.

---

## 8. Shipped Features & Roadmap

### Live in Classic Mode
- AI chatbot in sidebar (Claude, ChatGPT, Copilot, Gemini, Mistral)
- Smart Tab Groups (on-device ML, local inference)
- Link previews with AI-generated key points
- Shake to Summarize (iOS)
- AI controls panel with kill switch (Firefox 148, Feb 2026)
- Perplexity as secondary search option
- New Tab inferred personalization
- Translations, alt text in PDF viewer

### H2 2025 Roadmap (from strategy doc)
- Smart Tab Groups: Fx138, R100% 7/19
- Shake to Summarize: iOS Aug, Android Q4
- Link Previews: Fx140, R100% 8/5
- New Tab Inferred Personalization: Fx140, R100% 8/5
- 1-Click Chatbot Summarization: Fx141, R100% 9/2
- Semantic Search History: Fx141, R100% 9/2
- Multi-Modal on Desktop (TTS): Fx142, R100% 9/30
- Local Page Summarization: Fx145, R100% 12/23
- Video Summarizer: Fx146, R100% 12/23
- Q&A Page and Quick Answers: Fx145, R100% 12/23
- Address Bar Intent Detection: Fx144, R100% 11/25

### Feature Roadmap (from strategy deck, H2 25–H1 26)
**Committed (shipping H2 2025):**
- 1-Click Page Summarization
- Local Page Summarization
- Shake to Summarize

**In Evaluation (targeting H2 2025–H1 2026):**
- AI Read Aloud
- Ask an AI in Address Bar
- Page Q&A – Page Content Only
- Page Q&A – Internet Search Enabled
- Opt-in Consolidation
- Address Bar Content Classification

**In Discovery (long-term):**
- AI Mode — Strategic concept
- Agentic Workflow — Exploratory phase

---

## 9. AI Mode Concepts (from strategy deck)

These are the key UX concepts shown in the strategy deck for AI Mode:

### AI Compare
Split-view tab comparison with contextual recommendations. Supports making
complex tasks feel simple. Example: comparing Airbnb listings side-by-side
with an AI-generated comparison summary table and recommendation.

### Trip Planning Workspace
Plan an entire trip in a dedicated workspace. The assistant gathers tabs,
suggests next steps, shows context being used. Full itinerary, flights,
to-do lists, weather, bookmarks — all organized in one workspace.

### Summarize and Q&A (Mobile)
Cross-surface summarization with follow-up Q&A. Summary + Related Content
tabs. Mobile AI Mode with Search/Tabs/Past navigation.

### Helpful Memory, Low Effort
AI remembers context from previous sessions (with user control). Example:
recipe search → summarize results → find specific recipe → order ingredients
through Doordash — all facilitated by memory of dietary preferences.

### AI-Powered Content Flexibility
Transform content between formats (text → video, audio podcast, slideshow).
Save transformed content to organized folders. Cross-media browsing.

### Find and Buy (Agentic Commerce)
Natural language product search → curated results → one-tap purchase with
Apple Pay. Full commerce flow within AI Mode.

---

## 10. Investment Scenarios

For AI Mode specifically (from strategy deck):

| Scenario | Time to Ship | Team Size | Cost |
|----------|-------------|-----------|------|
| Base (pivot existing) | 12 months | Existing | None |
| Accelerated | 9-12 months | 16 HC | $5.5M/yr |
| Expanded | 9 months | 32 HC | $10.5M/yr |

Base scenario trade-offs: No additional hiring, significantly slows non-AI
Classic Mode development, pauses AI features for Classic Mode.

Accelerated: 1 PM, 1 EM, 14 Eng, 1 TPM. Continues Classic Mode value delivery.

Expanded: 2 PM, 2 EM, 28 Eng, 1 TPM. Pauses Classic Mode AI investment.

For the broader AI strategy (additional themes beyond core):
- 17 HC needed (2 PMs, 2 Designers, 4 Desktop Eng, 4 Mobile Eng, 5 MLEs)
- Hiring timeline: PM/Design/Eng 2-3 months, MLEs 3-5 months

---

## 11. Key Stakeholders & Teams

- **Tapan Kamdar** — Strategy driver for Firefox AI
- **Ajit Varma** — Mozilla VP of Product (public-facing AI messaging)
- **Anthony Enzor-DeMeo** — Mozilla CEO (appointed Dec 2025, "modern AI browser")
- **Jolie Huang** — Senior Product Manager (community engagement, AI controls)
- **Stefan Smagula** — Product Manager (Smart Tab Groups)
- **Jake Archibald** — Firefox developer (AI kill switch implementation)
- **Mark Surman** — Mozilla President ("rebel alliance" strategy)

Key teams: Firefox AI, Trust & Safety, Innovation Team (TABS), Growth/Onboarding,
Front-End, Platform & Accounts.

---

## 12. Design Constraints & Guardrails

### Privacy & Data
- Strict no-logging by default for local models
- No data-sharing with foundational model partners
- Explicit opt-in for remote AI usage with full transparency
- User data sent to cloud only with explicit consent
- Prompt-based usage ensures minimal, targeted data transfer
- Private Mode: on-device AI only, no cloud

### User Control
- Easy toggles for enabling/disabling AI features
- No forced adoption
- Individual feature management + full kill switch
- User preferences persist across updates
- Changeable at any time

### Financial
- AI features must show cost-effectiveness and clear ROI
- Cloud inference costs must be managed carefully

### Trust & Safety
- Human-in-the-loop design for sensitive tasks (purchases, form submissions)
- Transparent prompts about data usage
- Stress testing for harmful content generation
- Word blocklist based on open-source list
- Pre-release evaluation of emergent risks
- Technical red teaming for prompt injection and security vulnerabilities

### Technical
- Cross-platform: must work on Windows, Mac, Linux
- Performance: local AI can cause high CPU/battery (see Smart Tab Grouping issues)
- Model size: LoRA adapters to manage memory with multiple specialized tasks
- WebGPU support available from Firefox 141

### AI Adoption Context
- 91% of "Principled Trailblazers" already use AI tools
- 86% of students use AI to study
- 60% only use GenAI on topics they can verify
- Only 33% believe they can spot GenAI inaccuracies
- 30% report difficulty using GenAI as a concern
- 62% of Principled Trailblazers pay for at least 1 AI tool
