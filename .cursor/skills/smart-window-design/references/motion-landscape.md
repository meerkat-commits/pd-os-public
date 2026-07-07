# Motion Design Competitive Landscape & Resources

Research foundation for Smart Window's motion identity. Covers AI browsers,
AI chat products, best-in-class motion systems, UX motion principles, and
motion design tooling.

Last updated: March 2026

## Table of Contents

1. AI Browser Competitors
2. AI Chat Product Motion
3. Best-in-Class Motion Systems
4. Firefox Motion History
5. UX Motion Design Principles
6. Motion Design Tooling & Resources
7. Macro Trends (2025–2026)
8. Strategic Positioning for Smart Window

---

## 1. AI Browser Competitors

### Dia (The Browser Company)

**Design lead:** Charlie Deets (ex-Apple Safari, WhatsApp, Facebook)

**Motion philosophy: "Novelty budget."** The browser itself stays familiar
and restrained. Motion and color are deployed strategically at AI
interaction points to "express the power available to you in your
actions." Dia's overall design is "quite restrained" — motion is reserved
for Chat features where familiarity is less useful because patterns are
still emerging.

**Key motion patterns:**
- **Chat sidebar opening:** "Brand animation swells into the view" to
  signal AI assistant availability and that page context will be used.
  This is an intentional moment of brand expression at the AI seam.
- **Tab attachment piles:** When mentioning multiple tabs, they stack in
  an animated pile. Hovering the pile causes "playful animation." Clicking
  reveals all tabs. Described as "mostly superfluous but aims to reinforce
  the value of adding context."
- **Assistant Bar:** "Fluidly animated" as the most commonly used UI
  element. Smooth transitions prioritized here.
- **Page color extension:** Active tab UI inherits page color to
  reinforce relationship between browser and tab contents.
- **@ mention interaction:** Familiar social media pattern — type @ to
  reference tabs, history, bookmarks. Leaning into familiarity.

**What they call "elevated":** Familiar browser patterns with extra craft
and convenience layered on top — "only when it provides value above and
beyond what a user is expecting."

**"Tuesday morning" technique:** Everything should be familiar enough
that anyone can switch to Dia at 10am on a Tuesday morning without
learning new workflows.

**Strengths:** Strong product instinct, clear strategic framework
(novelty budget), high craft from ex-Apple designer. Good articulation
of when to be restrained vs. expressive.

**Weaknesses:** Not a documented motion system — designer craft
decisions, not replicable primitives or tokens. No published motion
grammar. Won't scale without systematization.

Source: browsercompany.substack.com/p/the-strategy-behind-dias-design

### Perplexity Comet

**Brand identity by:** Studio Freight, with Henry Modisett and Phi Hoang
(Perplexity Heads of Design and Brand Experience)

**Motion philosophy: Brand spectacle over product system.** Cosmic
themes — "parabolic lines inspired by orbital paths created paths for
motion throughout the system." Variable font weights expand on hover,
creating "a living material that stretches and reshapes with user
interaction." The in-product motion system is thin compared to the
brand layer.

**Key motion patterns:**
- **Variable type on hover:** PP Editorial New serif weights expand,
  creating "a living material" — a nod to cosmic expansiveness
- **Sidecar panel:** Right-side AI assistant with standard slide-in
- **Blue outline on tabs:** When the agent takes control of a tab, a
  blue outline confirms it is in control
- **Logo animation:** "Opens like a book to a new page"
- **Cosmic-to-earthbound scroll:** Website moves from space to Earth
  as users scroll; announcement video reverses this path

**Design language:** "Soft, balanced, and aesthetically consistent" with
accent colors, rounded corners — "sleek without being sterile. It's not
just minimalism. It's taste."

**Strengths:** Strong brand identity, distinctive visual language,
clear emotional direction.

**Weaknesses:** Brand-forward but product motion is thin. More mood
than grammar. No documented motion tokens or replicable system.

### Google Chrome (with Gemini)

Chrome itself uses Material Design 3 motion guidelines. The AI Overviews
loading animation shows phased states: "Searching..." → "Generating..."
→ "Putting it all together" with a pulsating blue/purple spotlight.
Gemini's product-specific motion is covered below.

---

## 2. AI Chat Product Motion

### Google Gemini

**The most articulated motion system of any AI product.** Google Design
published a deep-dive on their approach.

**Motion philosophy: Gradient as character.** Amorphous, pulsing color
gradients morph to represent thinking, listening, and responding. The
gradient is the AI's visual presence — it's how Gemini "looks alive."

**Core principles:**
- Each animation has a defined start and end point, creating directional
  flow that mirrors user actions
- Inner activity within motion conveys thinking, analysis, and
  intelligence, making processing feel transparent
- Motion allows users to see information coming together, visualizing
  conversations and listening abilities
- "When a system is hard to approach, the design must be soft"
- The speed of movement gives a sense of anticipation, then release

**Key patterns:**
- **Thinking state:** Morphing gradient shapes inspired by Material 3
  Expressive. Concentrated gradients pulse and shift while processing.
- **Voice input:** Rippling motion in radial gradients for voice waves.
  Concentrated and diffused gradients for transcribing.
- **Loading phases:** "Searching..." → "Generating..." → "Putting it
  together" — progressive state communication, not a single spinner
- **Feature introduction:** Gradients guide user's eye to introduce
  feature icons with directional motion
- **Foundational shape:** The circle — "simplicity, harmony, and
  comfort." Gemini's logo is constructed from four adjoining circles.

**Design philosophy on softness:** "This process highlights the
importance of a foundational experience that forgives mistakes,
anticipates confusion, and invites exploration. When a system is hard
to approach, the design must be soft. This softness — conveyed through
guided, pulsing gradient shapes, clear language, and transparent
signaling — allows users to engage with the new system feeling secure
and supported."

**Strengths:** Most documented AI motion system. Strong brand connection.
Philosophically grounded.

**Weaknesses:** Strongly Google-branded — gradient-as-character is hard
to differentiate from. Optimized for standalone chat, not browser-in-AI.

Source: design.google/library/gemini-ai-visual-design

### ChatGPT (OpenAI)

**Motion philosophy: Anthropomorphism through tempo.**

The most influential pattern in AI: delays between words make it feel
as if the computer is "thinking" and "deliberating." One developer
described it as "simply delightful anthropomorphism."

**Key patterns:**
- **Word-by-word text reveal** with variable timing — probabilistic
  delays simulate "thinking through" certain words
- **Blinking cursor** indicates AI "presence" — appears and disappears
  to show the AI is "there"
- **Shimmer/loading bar** for processing states
- **Sparkle icon** for AI-enhanced actions — now the industry-wide
  symbol, criticized as ubiquitous and losing meaning

**What they pioneered:** The *tempo* of AI conversation. The rhythm of
text appearing. The feeling that you're watching something think.

**Strengths:** Set industry patterns. Defined how people expect AI
conversation to feel.

**Weaknesses:** No published motion system — emergent, not architected.
The sparkle-shimmer idiom is now generic.

### Meta AI (Instagram, WhatsApp, Messenger)

**No published motion design system.** Motion craft in products but no
public documentation.

**Key patterns:**
- **Blue-purple gradient ring** as thinking/processing indicator
- **Streaming text reveal** for responses
- **Image generation progress** animations
- **In Instagram DMs:** slide-up transition with blue gradient accent

**Relevance to Smart Window:** Meta demonstrates the "AI as guest in
host product" pattern — AI living inside Instagram, not being Instagram.
The same tension Smart Window faces: AI inside a browser, not being the
browser. Their approach is clean but not distinctive.

---

## 3. Best-in-Class Motion Systems

### IBM Carbon Design System

**The gold standard for documented motion architecture in production.**

**Core framework: Productive vs. Expressive motion.**
- **Productive:** Quick, efficient, subtle — for microinteractions when
  the user needs to focus on tasks. Button states, dropdowns, revealing
  information, rendering data. Significantly faster than expressive.
- **Expressive:** Enthusiastic, vibrant, visible — for significant
  moments. Opening a new page, primary action buttons, system alerts,
  notifications. Captures attention and offers rhythmic breaks.
- **Philosophy:** "The motion curves are designed to reflect the duality
  of man and machine. Productivity and expression are both essential."
- **Guidance:** "Reserve expressive motion for occasional, important
  moments, to better capture the user's attention and offer a rhythmic
  break to the productive experience."

**Technical specifics:**
- Three easing types: standard, entrance, exit
- Each type available in both productive and expressive modes
- Dynamic duration: calculated based on style and size of motion.
  Non-linear duration scale for perceived consistency.
- Motion Generator tool for calculating custom element durations
- Shipped as code package: `@carbon/motion` with named tokens
  accessible via Sass and JavaScript

**Key insight:** "The best interface motion may go unnoticed, because
it often keeps users engaged with their tasks. Is your motion frequently
noticed by average users? If so, consider removing or minimizing it."

**Assessment framework for motion in products:**
1. Define the goals and values of the product
2. Assign productive or expressive motion to each interaction
3. Check for continuous elements in large transitions
4. Verify effectiveness across screen sizes
5. Ensure motion works with reduced-motion settings

**Relevance to Smart Window:** The productive/expressive duality maps
directly to Smart Window's architecture. Classic Mode = productive.
AI Mode = expressive at AI seams, productive everywhere else. The idea
that motion tokens ship as code, not just specs — that's the standard.

Source: carbondesignsystem.com/elements/motion/overview/

### Emil Kowalski (Linear / ex-Vercel)

**The most credible practitioner voice in product motion right now.**
Design engineer at Linear, previously Vercel. Creator of animations.dev
course, Sonner (toast library), and Vaul (drawer library).

**Philosophy: Restraint, speed, purposeful motion.**
- "I usually use the 'easeOut' curve for enter and exit transitions.
  The acceleration at the beginning gives the user a feeling of
  responsiveness."
- "I use a duration no longer than 0.3/0.4 seconds to keep the
  animation fast."
- "It's easy to start adding animations everywhere. The user then
  becomes overwhelmed and animations lose their impact."
- Linear animations are "rarely used, they feel robotic and unnatural
  as almost nothing in the world around us moves at a constant speed."
- Spring animations or real-world easing make animation "feel familiar
  and less artificial."
- "Speed of our animations can also alter the perceived performance of
  your app."

**Practical patterns from his libraries:**
- **Sonner (toast):** Stacked toasts with spring physics, smooth
  enter/exit, responsive to gesture
- **Vaul (drawer):** Mobile drawer with native-feeling easing, smooth
  snap points, gesture-driven physics

**Relevance to Smart Window:** Emil's restraint philosophy should be
the baseline for browser chrome motion. The browser itself moves with
Linear-level speed and restraint. The AI layer gets a different
vocabulary — but even there, restraint is the foundation.

Source: emilkowal.ski, animations.dev

### Apple Human Interface Guidelines

**Motion philosophy: Physics, not decoration.**

Elements have weight, momentum, spatial relationships. Motion
communicates layer relationships and state changes.

**Key principles:**
- Ideal animation duration: 100ms–500ms for most situations
- iOS 26 Liquid Glass: motion communicates depth and layer relationships
  through scaling, opacity, and spatial layering
- "Speed, rhythm, and weight of animations are becoming as important as
  colors and typography"
- "Micro-interactions will increasingly be the place where brand
  identity is felt — not just seen"
- visionOS: motion comfort guidelines — avoid oscillations (especially
  ~0.2 Hz), provide stability, be gentle with camera motion, respect
  reduced motion accessibility

**visionOS-specific insights relevant to Smart Window:**
- Content requiring extended reading should be placed center and
  slightly below line of sight
- Slow transitions between brightness levels for comfort
- Provide reduced-motion alternatives, not just disabled motion
- Make content semitransparent when motion cannot be avoided

**Relevance to Smart Window:** Motion as physics, not personality.
Firefox runs on all platforms — motion needs to feel physically grounded.
The accessibility rigor: `prefers-reduced-motion` is a first-class
design consideration, not an afterthought.

### Material Design 3 (Google)

Distinct from Gemini's product-specific motion. Material 3 Expressive
introduced new shape and motion concepts. Relevant as the system
Firefox's competitors (Chrome-based browsers) inherit by default.
Material defines three motion principles: informative, focused,
expressive — with four uses: hierarchy, feedback, status, character.

---

## 4. Firefox Motion History

### Firefox Quantum Motion (2018)

The only documented Firefox motion work. Created by Amy Lee and Eric
Pang — two designers who formed an informal "motion team" by making a
sticker and calling themselves one.

**Three principles:** Quick, Informative, Whimsical.
- **Quick:** Prioritize perceived performance over technical benchmarks.
  Animations should be fast and nimble, never keeping users waiting.
- **Informative:** Aid flow of actions, give clear guidance for user
  orientation — spatial and temporal.
- **Whimsical:** Playful personality elements, even in a browser.

**Process:** After Effects → Bodymovin → JSON → custom tool (by Markus
Stange) → SVG sprite sheets → CSS animations. Custom motion curve for
tabs and menus.

**What they shipped:** Download icon animation, bookmark star animation,
page reload icon, tab transitions, menu animations.

**Limitations for Smart Window:** These principles were designed for
icon-level animations in a traditional browser. They don't address:
thinking states, confidence signaling, conversational rhythm, handoff
choreography, memory recall, mode transitions, or the "alive but not
human" tension that AI products require. The principles still apply to
Classic Mode microinteractions but need extension for AI territory.

### Acorn Design System Principles (current)

Firefox's current design principles (not motion-specific):
- **Crafted with care:** Every detail necessary, clear, polished
- **Delightful:** Warm, approachable, charm and whimsy, soul — "designed
  by people, for people"
- **Empowering:** Meaningful choices, clarity, control, calm — "I feel
  in control with Firefox"
- **Trailblazing:** Push boundaries, effortless, intuitive, responsive

These are brand principles, not motion principles. They inform motion
direction but don't specify it. "Delightful" doesn't spec an easing
curve. "Trailblazing" doesn't tell you what happens when the AI is
thinking.

---

## 5. UX Motion Design Principles

Foundational principles that inform any motion system, synthesized from
industry practice, academic research, and the best production systems.

### Purpose-Driven Motion

Every animation must serve at least one functional purpose:
- **Feedback:** Confirming that user action was received
- **Orientation:** Showing where the user is in the system
- **Continuity:** Maintaining context during state changes
- **Hierarchy:** Drawing attention to what matters most
- **Teaching:** Demonstrating how interactions work
- **Status:** Communicating system state (loading, processing, error)

Motion that serves none of these purposes is decoration. Decoration
should be rare and intentional.

### Duration & Timing

Industry consensus on animation timing:
- **Micro-interactions (feedback):** 100–200ms — fast enough to feel
  instant, slow enough to be perceived
- **Simple transitions (state changes):** 200–300ms — the sweet spot
  for most UI transitions
- **Complex transitions (layout shifts):** 300–500ms — needed for
  larger spatial movements
- **Emphasis moments (AI thinking, onboarding):** 500ms–1000ms —
  reserved for moments that need attention
- **Anything over 1 second** risks feeling slow unless it's continuous
  (like a loading state)

Dynamic duration: larger movements need longer durations. A sidebar
sliding 400px needs more time than a button changing color.

### Easing as Emotional Tone

Easing curves communicate character:
- **EaseOut (decelerate):** Responsive, confident. Element arrives
  quickly and settles. Best for most enter transitions. Emil Kowalski's
  default choice.
- **EaseIn (accelerate):** Departing, releasing. Element starts slow
  and speeds up as it leaves. Best for exit transitions.
- **EaseInOut:** Smooth, considered. Best for state changes where the
  element stays visible throughout (expanding, repositioning).
- **Linear:** Mechanical, robotic. Almost never appropriate for UI.
  Exception: progress indicators where constant speed = honesty.
- **Spring:** Physical, natural, alive. Best for direct-manipulation
  responses (drag, gesture). Can feel bouncy if overdone — use
  critically-damped springs for product UI, underdamped only for
  playful contexts.
- **Custom cubic-bezier:** Brand-specific curves. Smart Window's
  existing carousel uses cubic-bezier(0.5, 0, 0.2, 1).

### Spatial Logic

Elements should have clear spatial origins and destinations:
- Panels slide from the edge they're anchored to
- Dropdowns expand from the trigger that opened them
- Chips scale from their insertion point
- Modals can scale from center (emphasis) or slide from edge (spatial)
- Deleted items exit toward their source (undo tray, trash)

Appearing from nowhere or disappearing into nothing breaks spatial
logic. When an element has no logical origin, use opacity (fade) rather
than spatial movement.

### Choreography & Sequencing

When multiple elements animate together:
- **Primary first:** The most important element leads
- **Stagger:** Secondary elements follow with small delay (40–80ms)
- **Shared timing:** Elements that belong together move together
- **Interruption:** New interactions should interrupt and redirect,
  not queue behind current animations
- **Reduced motion:** All choreography must have a reduced-motion
  equivalent that preserves meaning without movement

### Accessibility (prefers-reduced-motion)

Non-negotiable baseline:
- Every animation must have a reduced-motion fallback
- Reduced motion ≠ no motion. Transform to non-movement equivalents:
  sliding → instant position change with crossfade, pulsing → static
  with subtle opacity, streaming text → block appearance
- Design the reduced-motion experience first, then add motion on top
- If the interface doesn't work without animation, the animation is
  load-bearing in a way that excludes users
- WCAG 2.3.3: Motion triggered by interaction can be disabled
- WCAG 2.2.2: Moving/scrolling content needs pause/stop mechanism
  if it lasts > 5 seconds and runs alongside other content
- No content flashing > 3 times per second

---

## 6. Motion Design Tooling & Resources

Reference tooling for prototyping, implementing, and refining motion
design across the Smart Window product surface.

### Animation Libraries

**Motion (formerly Framer Motion)** — motion.dev
The dominant React animation library. Declarative API, layout
animations, gesture support, spring physics, exit animations via
AnimatePresence. Used by Linear, Vercel, and many production apps.
Key features: `animate`, `whileHover`, `whileTap`, `layout`,
`layoutId` for shared element transitions, `useAnimate` for imperative
control. ~12kb for layout animations.

**Anime.js** — animejs.com
All-in-one JavaScript animation engine (v4). 24.5kb total, modular.
CSS transforms, SVG morphing/drawing/motion paths, scroll observer,
advanced staggering (grid-based, center-out), spring physics,
draggable API, timeline sequencing, responsive scopes with media
queries. Works with any framework or vanilla JS.

**GSAP (GreenSock)** — gsap.com
Industry-standard animation platform. Complex timelines, scroll-driven
animations, morphing, text splitting. Highest performance ceiling.
Heavier than alternatives but most capable for complex sequences.

### React Component Libraries

**React Bits** — reactbits.dev
Animated UI component library for React. Pre-built interaction
components (animated cards, text effects, transitions) that can be
used as prototyping references or starting points.

**React Haiku** — reacthaiku.dev
Lightweight React hook and utility library (46 hooks, 9 utilities,
<7kb). Includes interaction-relevant hooks: `useLeaveDetection`,
`useClickOutside`, `useDebounce`, `useHold`. Useful for interaction
state management alongside animation.

### Design & Prototyping Tools

**Unicorn Studio** — unicorn.studio
No-code WebGL design tool. Layer-based workflow (like Figma) that
compiles to WebGL shaders. 70+ configurable effects, motion and
interactivity as core features (not afterthoughts). Any layer property
can respond to events: scroll, hover, mouse, appear. Lightweight
runtime (~36kb gzipped). Useful for exploring AI presence effects,
gradient behaviors, and ambient motion without writing shader code.
Embeds into Framer, Webflow, or custom sites.

**Rive** — rive.app
Interactive animation tool with state machines. Embeds logic into
animations (hover → play, click → switch state) without code. Real-time
updates, small runtime. Strong for complex interactive animations like
loading states, thinking indicators, and multi-state UI elements.

**Lottie** — lottiefiles.com
After Effects → lightweight JSON animation format. Plays natively on
web, iOS, Android. Good for icon animations and microinteractions.
The format Firefox Quantum used (via Bodymovin) for their 2018 motion
work.

### Learning & Reference

**animations.dev** — Emil Kowalski's course
Comprehensive course on web animation: easing theory, Framer Motion
patterns, taste development, practical component builds (drawer, toast).
Split into theory ("making it feel right"), implementation ("how I use
Framer Motion"), and details ("the big little details").

**easing.dev**
Visual easing curve explorer. Browse and compare named curves
(Anticipate, Quick Out, Overshoot Out, Swift Out, Snappy Out, all
standard In/Out/InOut variants). Both cubic bezier and spring previews.
Useful for selecting and communicating easing choices.

### Implementation Reference

**CSS Animations & Transitions**
Firefox's XPFE frontend is HTML/JS/CSS on Gecko. CSS is the
lowest-overhead option for simple transitions. Key properties:
`transition-property`, `transition-duration`, `transition-timing-function`,
`animation-name`, `animation-duration`, `animation-iteration-count`.
Always animate only `transform` and `opacity` for GPU compositing.
Use `will-change` sparingly.

**Web Animations API (WAAPI)**
Native browser API for programmatic animation. No library needed.
Supported in all modern browsers including Firefox. Motion (Framer
Motion) can use WAAPI as its backend for smaller bundle size.

**`@media (prefers-reduced-motion: reduce)`**
CSS media query for respecting user motion preferences. Firefox honors
this across all platforms (GTK/GNOME, KDE, Windows, macOS, iOS,
Android). Can also be set via `about:config` preference
`ui.prefersReducedMotion`.

---

## 7. Macro Trends (2025–2026)

**Restraint over spectacle.** "Motion in 2026 isn't about adding energy
for its own sake. It's about making communication clearer and more
accessible." Animations are "no longer used to impress users."

**Purpose over decoration.** Motion is a strategic design tool, not
polish. Every animation should reinforce function.

**Physics over personality.** Organic motion — elastic easing, curved
paths, varied timing that mimics breathing patterns — "subconsciously
connects with trustworthiness and authenticity. Robotic, linear feels
corporate and cold."

**Systems over one-offs.** Companies need motion that scales — tokens,
named curves, reusable primitives shipped as code.

**Taste as differentiator.** "What AI cannot yet do is curate, refine,
and select the choices that give a piece emotional resonance." Good
taste in motion is the new competitive advantage.

**The sparkle fatigue.** The four-pointed star/sparkle has become the
generic AI signifier. Ubiquitous to the point of meaninglessness.
Users are underwhelmed, not delighted. One industry critique: the
sparkle promises "magic" for technology that doesn't always deliver,
creating expectation mismatch.

**Imperfection as signal.** "In a digital environment where so much
content is generated, optimized, and refined by machines, visual
perfection is no longer impressive. Small irregularities, visible
textures, and expressive details signal that a human was involved."

---

## 8. Strategic Positioning for Smart Window

### What competitors do

Everyone uses motion to make AI feel impressive, alive, magical:
- **Gemini:** gradient-as-thinking-state (softness as trust)
- **ChatGPT:** anthropomorphic tempo (feeling of talking to a person)
- **Dia:** playful novelty budget (delight at AI seams)
- **Comet:** cosmic brand spectacle (aspiration)
- **Meta AI:** generic blue gradient ring (utility)

### What nobody does

No competitor has built a motion system designed for a **privacy-first
AI browser** that communicates **trust through transparency, not delight
through spectacle.** No one has:
- Published motion tokens for an AI browser product
- Defined the productive/expressive split for AI-in-browser specifically
- Addressed the "AI as guest in host product" tension systematically
- Built motion serving three distinct personas simultaneously:
  Josef (privacy-conscious, wants predictability and visible control),
  Mina (busy multitasker, wants motion she barely notices), and
  Avery (Gen Z, wants the product to feel alive and modern)
- Created motion that's "alive enough to be almost human but the user
  knows it's not"
- Accounted for the "trust tax" — Firefox's audience chose the browser
  because of values, so every AI feature (and its motion) must earn
  trust before it can deliver delight

### Smart Window's motion gap to own

**Honest presence with rhythm.** Motion that communicates what the
system is actually doing. Not sparkles. Not gradients. Not magic. You
can see when it's thinking, when it's responding, when it's uncertain,
and the motion never oversells what's happening underneath.

**Four reference models to synthesize:**
1. **Carbon's rigor** — two motion modes, tokenized curves, dynamic
   duration, shipped as code
2. **Emil Kowalski's restraint** — fast, invisible, purposeful, never
   performing
3. **Apple's physics** — weight, momentum, spatial continuity,
   accessibility-first
4. **Gemini's AI-state communication** — phased thinking states
   (without the gradient-as-identity approach)

---

## 7. Implementation Tooling

For detailed descriptions and when to use each, see
`ux-motion-foundations.md` section 8. Quick reference:

| Tool | Type | Use Case |
|------|------|----------|
| Motion (motion.dev) | React animation library | Production animation, springs, gestures, layout |
| Anime.js (animejs.com) | JS animation engine | Framework-agnostic animation, SVG, stagger, timelines |
| React Bits (reactbits.dev) | Component library | 110+ animated React components for rapid prototyping |
| React Haiku (reacthaiku.dev) | React hooks | Interaction detection (hover, viewport, mouse, media query) |
| animations.dev | Learning resource | Emil Kowalski's motion craft course |
| easing.dev | Reference tool | Easing curve visualization and comparison |
| Unicorn Studio | WebGL design tool | Visual effect prototyping (gradients, shaders, motion) |

**Firefox implementation note:** Smart Window's frontend is HTML/JS/CSS
on Gecko (XPFE), not React. These tools serve as prototyping references
and specification aids. Final implementation uses CSS animations, CSS
transitions, and vanilla JS within Firefox's architecture. Motion tokens
should be defined as CSS custom properties and JS constants.
