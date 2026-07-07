# UX & Motion Design Foundations

Foundational UX principles, motion design theory, easing fundamentals, and
implementation tooling for the Smart Window motion design system. This
document is framework-agnostic — it covers the *why* and *what* of motion
design. Surface-specific *how* is in the design system and pattern specs.

Last updated: March 2026

## Table of Contents

1. UX Principles That Govern Motion
2. Motion Design Theory
3. Easing Fundamentals
4. Duration & Timing
5. Choreography & Sequencing
6. Accessibility & Reduced Motion
7. Performance Constraints
8. Implementation Tooling & References

---

## 1. UX Principles That Govern Motion

Motion is not a layer applied after interaction design is complete. It is
interaction design. Every animation decision is a UX decision.

### 1.1 Feedback & Acknowledgment

Every user action deserves a response. Motion confirms that the system
registered an input. Without feedback, users repeat actions, lose
confidence, and abandon flows. The feedback should be proportional to the
action — a button press gets a subtle scale change, a major state
transition gets a visible spatial animation.

**Principle:** The smaller and more frequent the action, the faster and
more subtle the feedback. The larger and rarer the action, the more
visible the response.

### 1.2 Orientation & Wayfinding

Motion shows users where they are, where they came from, and where they
can go. Spatial transitions (slide left/right, expand from origin,
collapse to destination) maintain the user's mental map of the interface.
Without spatial continuity, every state change feels like a teleport.

**Principle:** Elements should arrive from a direction that makes spatial
sense and depart in a direction that preserves context. New content
entering from the right implies forward progression. Panels sliding from
their anchored edge confirms their spatial position.

### 1.3 Hierarchy & Attention

Motion directs the eye. The first element to move gets the most attention.
Staggered entrances create reading order. Larger movements draw focus away
from smaller ones. Motion establishes which element matters most at any
given moment.

**Principle:** Primary content animates first. Secondary content follows
with a slight delay. Background changes happen simultaneously or not at
all. Never animate everything at once — it creates visual noise, not
hierarchy.

### 1.4 State Communication

Motion distinguishes between states. A loading animation differs from an
error animation differs from a success animation — not just in icon or
color, but in movement quality. Smooth, continuous motion suggests progress.
Abrupt stops suggest failure. Gentle settling suggests completion.

**Principle:** The character of the motion should match the character of
the state. Thinking is rhythmic and ongoing. Success is a clean resolution.
Error is a clear but non-alarming interruption. Uncertainty is slower and
less committed than confidence.

### 1.5 Perceived Performance

Users judge speed by feel, not by clock. A 300ms animation with an easeOut
curve feels faster than a 200ms animation with linear timing because the
element appears to arrive quickly and settle naturally. Skeleton states,
progressive loading, and optimistic UI updates all use motion to make the
interface feel faster than it technically is.

**Principle:** Show something immediately. Animate the arrival, not the
waiting. Display the user's sent message before the AI responds. Show
the thinking state instantly when the query is submitted. Never let the
user stare at a static screen wondering if their action was received.

### 1.6 Progressive Disclosure

Motion can reveal complexity gradually. Expanding panels, cascading content,
and staged information delivery prevent cognitive overload. The interface
shows what matters first, then reveals detail on demand.

**Principle:** Animate the reveal, not just the content. A panel that
expands from its trigger point teaches the user where it lives. Content
that fades in after a heading teaches the user what belongs together.

### 1.7 Trust & Predictability

Consistent motion builds trust. When the sidebar always animates the same
way, users stop watching it and start using it. When animations vary
unpredictably, users become uncertain about what will happen next. Trust
is built through repetition, broken by surprise.

**Principle:** Establish patterns early and repeat them consistently. The
same type of action should always produce the same type of motion. If a
chip enters from below with a fade, all chips enter from below with a fade.
Deviations require justification.

### 1.8 Emotional Calibration

Motion carries emotional weight. Fast, snappy motion feels efficient and
professional. Slow, flowing motion feels calm and premium. Bouncy motion
feels playful and informal. The emotional tone of the motion should match
the emotional context of the interaction.

**Principle:** Match motion character to context. Error states should not
bounce. Celebratory moments should not be clinical. AI thinking states
should feel neither rushed nor lethargic — they should communicate active
processing at a human-readable pace.

---

## 2. Motion Design Theory

### 2.1 The 12 Principles of Animation (Applied to UI)

Disney's 12 principles, adapted for interface motion:

**Timing:** The duration of an animation communicates weight, importance,
and urgency. Short = responsive, long = considered.

**Ease in / Ease out (Slow in / Slow out):** Natural motion accelerates
and decelerates. Linear motion looks robotic. UI elements should ease out
of rest (accelerate) and ease into their destination (decelerate).

**Anticipation:** A small movement before the main action (e.g., a button
compressing slightly before expanding to a modal) signals what is about
to happen. Use sparingly in productivity UI.

**Follow-through:** Elements settle into position rather than stopping
abruptly. A panel that overshoots slightly and settles back feels more
natural than one that stops dead. Springs create this effect.

**Staging:** Direct the user's eye to the most important action. Only one
thing should be demanding attention at any given time.

**Secondary action:** Supporting animations that accompany the main
action without competing for attention. Background dimming while a modal
opens. Content reflowing while a sidebar expands.

**Arcs:** Natural motion follows curved paths, not straight lines. Less
relevant in flat UI, but applicable to spatial transitions and gesture-
driven interactions.

**Exaggeration:** Amplifying movement for clarity. A chip that scales up
slightly before disappearing is more noticeable than one that simply
vanishes. Use judiciously — exaggeration in UI can feel cartoonish.

### 2.2 Productive vs. Expressive Motion (IBM Carbon Model)

The most rigorous framework for categorizing UI motion:

**Productive motion** — fast, efficient, subtle. Used for microinteractions
where the user needs to focus on their task: button states, dropdowns,
revealing information, rendering data. The motion gets out of the way.

**Expressive motion** — deliberate, vibrant, visible. Used for significant
moments where the system needs the user's attention: page transitions,
primary action feedback, notifications, onboarding moments. The motion
demands a beat of attention.

**The relationship:** Reserve expressive motion for occasional, important
moments. If everything is expressive, nothing is. The contrast between
productive and expressive creates rhythm.

**For Smart Window:** Browser chrome (tabs, toolbar, navigation) = always
productive. AI interaction seams (sidebar opening, thinking state, first
response, memory application) = expressive. The boundary between
productive and expressive IS the boundary between browser and AI.

### 2.3 The Novelty Budget (Dia / Browser Company Model)

Every product has a limited amount of user attention available for learning
new patterns. The "novelty budget" concept says: spend it where it
matters most.

**For Smart Window:** The browser is familiar — tabs, back/forward, URL
bar, bookmarks. Don't spend novelty budget here. AI interactions are new —
the sidebar, the chat, the thinking state, memories. Spend the budget here.
The motion language for familiar browser elements should be invisible. The
motion language for AI elements should be noticeable enough to teach users
how they work.

### 2.4 Restraint Doctrine (Emil Kowalski / Linear)

The most respected practitioner philosophy in current product motion:

- Duration no longer than 300-400ms for standard interactions
- easeOut for enter and exit transitions (fast start, gentle settle)
- Spring physics only for direct-manipulation gestures (drag, swipe)
- "It's easy to start adding animations everywhere. The user then
  becomes overwhelmed and animations lose their impact."
- The best motion goes unnoticed — it makes the interface feel responsive
  without calling attention to itself

**For Smart Window:** This is the baseline. Before making any animation
more elaborate, ask: does Emil Kowalski restraint-level motion already
accomplish the goal? If yes, don't add more.

---

## 3. Easing Fundamentals

### 3.1 Why Easing Matters

Easing defines how an animation's speed changes over time. It is the
single most impactful variable in motion quality. The same duration with
different easing produces completely different emotional effects.

**Linear** — constant speed. Looks robotic and unnatural. Almost never
appropriate for UI motion. Only used for continuous loops (loading
spinners, progress bars).

**Ease-out** — starts fast, decelerates. The most common UI easing. Makes
elements feel responsive (they react immediately) and natural (they settle
into place). Use for elements entering the viewport.

**Ease-in** — starts slow, accelerates. Use for elements leaving the
viewport (they gather speed as they exit). Rarely used on its own.

**Ease-in-out** — slow start, fast middle, slow end. Use for elements
that remain on screen while changing (position shifts, size changes,
color transitions). The symmetry feels balanced and controlled.

### 3.2 Cubic Bezier Notation

CSS easing is defined with `cubic-bezier(x1, y1, x2, y2)` where:
- (x1, y1) is the first control point
- (x2, y2) is the second control point
- x values must be 0-1 (representing time)
- y values can exceed 0-1 (creating overshoot/bounce effects)

Common curves:
- `ease`: cubic-bezier(0.25, 0.1, 0.25, 1.0) — CSS default
- `ease-in`: cubic-bezier(0.42, 0, 1.0, 1.0)
- `ease-out`: cubic-bezier(0, 0, 0.58, 1.0)
- `ease-in-out`: cubic-bezier(0.42, 0, 0.58, 1.0)

**Smart Window's current documented curve:**
- Placeholder carousel: cubic-bezier(0.5, 0, 0.2, 1) — an aggressive
  easeOut with a fast initial acceleration

### 3.3 Spring Physics

Springs simulate physical tension and release. Unlike cubic-bezier curves,
springs are defined by physical properties:
- **Stiffness** — how tight the spring (higher = snappier)
- **Damping** — how quickly oscillation settles (higher = less bounce)
- **Mass** — weight of the element (higher = more lethargic)

Springs are ideal for:
- Direct-manipulation interactions (dragging, swiping, flicking)
- Natural settling effects (a panel overshooting slightly and settling)
- Interruptible animations (the user can grab a spring-animated element
  mid-flight and the physics respond naturally)

Springs are NOT ideal for:
- Timed sequences (springs don't have a fixed duration)
- Choreographed multi-element transitions
- Precise timing requirements

### 3.4 The linear() CSS Function (Modern Easing)

The `linear()` CSS function allows complex easing curves that were
previously impossible without JavaScript. It accepts multiple stops to
approximate bounce, elastic, and other physics-based curves natively
in CSS. Useful for:
- Bounce effects without JavaScript
- Elastic settling without spring libraries
- Custom easing curves that match brand-specific motion feel

---

## 4. Duration & Timing

### 4.1 Duration Scale

Durations should be dynamic based on the size and type of animation:

**Instant (0-100ms):** Color changes, opacity toggles, focus rings.
Perceived as immediate. No easing needed.

**Fast (100-200ms):** Button feedback, tooltip appearance, small state
changes. Perceived as responsive. Simple easeOut.

**Standard (200-350ms):** Panel transitions, dropdown open/close,
suggestion appearance, chip enter/exit. The workhorse duration. easeOut
for enters, easeIn for exits, easeInOut for transforms.

**Considered (350-500ms):** Full sidebar open/close, page transitions,
major layout changes. Perceived as deliberate. Used for AI-seam moments
where you want the user to register the transition.

**Extended (500ms+):** Use only for continuous states (thinking animation
loops, loading indicators) or complex choreography (onboarding
sequences). Never for individual element transitions.

### 4.2 The 300ms Rule

Emil Kowalski's guidance: standard interactions should not exceed 300-400ms.
This maps to research showing that animations over 400ms start feeling
sluggish, while animations under 100ms are too fast to register as motion.

**Exception:** AI-specific moments can use 350-500ms because they represent
a shift in who is in control (human → machine or machine → human). The
slightly longer duration marks the boundary.

### 4.3 Stagger Timing

When multiple elements enter or exit together, stagger their timing:
- Per-element delay: 30-80ms between elements
- Total group duration should not exceed 300-500ms
- First element enters immediately; subsequent elements follow
- Limit staggered groups to 5-8 elements; beyond that, use a single
  group animation

---

## 5. Choreography & Sequencing

### 5.1 Enter/Exit Pairs

Every element that enters should have a corresponding exit. The exit
should be faster than the entrance (users care about what's arriving,
not what's leaving). Common pattern:
- Enter: 250ms easeOut
- Exit: 150ms easeIn

### 5.2 Interruption Behavior

What happens when an animation is interrupted by a new action?

**Replace:** Stop the current animation and start the new one from the
element's current position. Best for fast, frequent interactions (typing
in search, scrolling through suggestions).

**Queue:** Complete the current animation, then start the new one. Best
for sequential processes (onboarding steps, multi-stage flows).

**Blend:** Merge the new animation into the current one using spring
physics. Best for gesture-driven interactions (drag, swipe).

### 5.3 Concurrent vs. Sequential

**Concurrent:** Multiple elements animate at the same time. Feels fast
and cohesive. Use when the elements are semantically related (a panel
and its content entering together).

**Sequential:** Elements animate one after another. Feels deliberate and
staged. Use when you want to establish hierarchy (title first, then body,
then actions).

**Overlap:** Elements begin animating before the previous one finishes.
The best balance of speed and hierarchy. Standard stagger delay (30-80ms)
creates overlap naturally.

---

## 6. Accessibility & Reduced Motion

### 6.1 prefers-reduced-motion

This is a first-class design requirement, not a compliance checkbox.

When `prefers-reduced-motion: reduce` is set:
- Replace spatial animations (slides, scales) with opacity crossfades
- Replace continuous animations (pulses, loops) with static states or
  very subtle opacity shifts
- Replace complex choreography with instant state changes
- Preserve information that motion conveys through non-motion means
  (text labels, color changes, icon changes)

### 6.2 Design Reduced-Motion First

If the interface doesn't work without animation, the animation is
load-bearing in an exclusionary way. The design process should be:
1. Build the static states
2. Ensure information is clear without motion
3. Add motion to enhance, not to enable
4. Test with reduced-motion enabled

### 6.3 WCAG Requirements

- **2.2.2:** Moving content lasting >5 seconds must be pausable/stoppable
- **2.3.1:** Nothing flashes more than 3 times per second
- **2.3.3:** Motion triggered by interaction can be disabled

### 6.4 Vestibular & Cognitive Considerations

- Large-scale parallax and scroll-jacking can cause motion sickness
- Rapid direction changes and oscillations are uncomfortable
- Continuous peripheral animation is distracting for focus tasks
- Speed should never be so fast that state changes are imperceptible

---

## 7. Performance Constraints

### 7.1 Compositor-Safe Properties

For smooth 60fps animation, only animate properties that can be handled
by the browser's compositor without triggering layout or paint:

**Safe (compositor-only):**
- `transform` (translate, scale, rotate)
- `opacity`

**Expensive (triggers paint):**
- `background-color`, `box-shadow`, `border-radius`, `filter`

**Very expensive (triggers layout):**
- `width`, `height`, `padding`, `margin`, `top`, `left`

### 7.2 will-change

Use `will-change` to hint the browser about upcoming animations:
```css
.sidebar { will-change: transform; }
```
But remove it after the animation completes — permanent `will-change`
creates unnecessary GPU memory overhead.

### 7.3 GPU Acceleration

`transform: translateZ(0)` or `transform: translate3d(0,0,0)` forces
GPU acceleration. Use judiciously — it creates a new compositing layer
which consumes GPU memory.

### 7.4 Firefox-Specific Considerations

Smart Window runs on Gecko, not Blink or WebKit:
- Firefox's compositor has different performance characteristics
- CSS `contain` property helps isolate animated elements
- `content-visibility: auto` can improve off-screen animation perf
- Firefox supports `prefers-reduced-motion` natively across all
  platforms (GTK/GNOME, KDE, Windows, macOS)
- WebGPU available from Firefox 141

---

## 8. Implementation Tooling & References

### 8.1 Animation Libraries

**Motion (motion.dev)** — Previously Framer Motion. The most widely adopted
React animation library (30M+ npm downloads/month). Declarative API,
spring physics, layout animations, gesture recognition, scroll-linked
animations. Hardware-accelerated using Web Animations API with JS
fallback for springs and interruptible keyframes. Used by Framer, Figma,
and major production apps. Emil Kowalski's primary tool.
→ https://motion.dev

**Anime.js (animejs.com)** — v4.0: lightweight, modular JavaScript
animation engine. Per-property parameters, advanced staggering, SVG
morphing/drawing/motion paths, scroll observer, draggable API, spring
physics, timeline orchestration, responsive scope with media queries.
Framework-agnostic — works with any JS setup. Modular imports keep
bundle size small.
→ https://animejs.com

### 8.2 Component Libraries

**React Bits (reactbits.dev)** — 110+ animated React components: text
animations, UI elements, backgrounds. Supports GSAP, Framer Motion, and
React Spring. Four variants per component (JS-CSS, JS-Tailwind, TS-CSS,
TS-Tailwind). Copy-paste ready or CLI install via jsrepo. Useful for
prototyping motion concepts quickly and exploring interaction patterns
before building custom implementations.
→ https://reactbits.dev

**React Haiku (reacthaiku.dev)** — Lightweight React hooks library.
Motion-relevant hooks include: useHover, useIntersectionObserver (viewport
detection for scroll-triggered animations), useMousePosition, useMediaQuery
(responsive animation), useKeyPress, useInterval (for timed sequences),
useLeaveDetection. Utility-focused — not an animation library itself, but
provides the interaction detection that triggers animations.
→ https://reacthaiku.dev

### 8.3 Learning & Exploration

**animations.dev** — Emil Kowalski's course on web animations. Covers
making animations feel right (easing, timing, restraint), Framer Motion
patterns, and the "big little details" that separate good from great
motion. The most respected practitioner resource for product-grade web
animation. Theory and implementation.
→ https://animations.dev

**easing.dev** — Curated collection of easing graphs. Visual reference
for comparing easing curves side by side. Useful during motion system
definition for selecting and documenting named easing tokens. See also:
easings.net (easing function cheat sheet), cubic-bezier.com (interactive
bezier editor).
→ https://www.easing.dev

### 8.4 Visual Effects & Prototyping

**Unicorn Studio (unicorn.studio)** — No-code WebGL design tool. 70+
shader effects (distortion, blur, depth, lighting, gradient morphs),
layer-based scene composition, interactive motion tied to scroll/hover/
mouse. 36kb gzipped runtime. Embeds into Framer, Webflow, or custom
sites. Useful for prototyping advanced visual effects (AI presence
indicators, gradient animations, ambient backgrounds) without writing
shader code. Not for production UI motion — for exploration and
visual concept development.
→ https://www.unicorn.studio

### 8.5 Additional References

**IBM Carbon Motion** — The gold standard for documented motion systems.
Productive/expressive duality, tokenized easing curves, dynamic duration
scale. Ships as @carbon/motion npm package.
→ https://carbondesignsystem.com/elements/motion/overview/

**Apple Human Interface Guidelines — Motion** — Physics-based principles,
duration recommendations (100-500ms), platform-specific guidance including
visionOS spatial motion and reduced-motion requirements.
→ https://developer.apple.com/design/human-interface-guidelines/motion

**Google Material Design — Motion** — Transition patterns, container
transforms, shared-axis transitions. The system Chrome-based competitors
inherit.
→ https://m3.material.io/styles/motion/overview

**NNGroup — Animation Duration & Motion** — Research-backed guidance on
timing, easing, and motion characteristics for usability.
→ https://www.nngroup.com/articles/animation-duration/

---

## Firefox Browser Chrome Motion Specs (Product Sprint)

Baseline motion behaviors for Classic Firefox browser chrome, defined
during a Mozilla product sprint. Smart Window intentionally deviates
from these to create presence, warmth, and the "illuminate" quality
that makes the AI feel alive.

### Classic Firefox Baseline (for reference)

These specs apply to Classic Window and Private Window. They prioritize
invisibility — fast, functional, get out of the way.

**Side Panels:** Expand in place, 200ms ease-out. Content static, revealed.
Exit: 180ms ease-in.

**Tabs:** Expand in place, 200ms ease-out. Static internals. Close: instant.

**Popups:** 24px travel + fade, 200ms ease-out. Exit: instant.

**Callouts:** 16px travel + fade, 200ms ease-in. Directional content:
Ease Out Back 120ms (the one permitted overshoot). Exit: instant.

**Anchored Bars:** Expand like panels. 200ms / 180ms.

Core spatial philosophy: expand not slide, content after container
(50ms delay), exits faster than entrances, ephemeral elements dismiss
instantly.

### Smart Window Deviations

Smart Window takes the sprint's spatial philosophy (expand not slide,
content after container, exits faster than entrances) but replaces
the timing, easing, and choreography to create a product that feels
alive, present, and warm.

**Why deviate:** Classic Firefox motion is designed to be invisible. Smart
Window's motion is designed to be *felt*. Not theatrical — felt. The
difference between a room with the lights off and a room where someone
left a candle burning. You notice the warmth without identifying what's
causing it.

**Sidebar: 320ms AI-register curve, staggered content settle**
Classic sidebar: 200ms ease-out, static content reveal.
Smart Window sidebar: 320ms with the organic AI-register curve. Content
fades in with 30ms stagger between items — the sidebar populates, it
doesn't just appear. The smartbar glow activates as the sidebar opens.
Exit: 240ms browser curve. Not instant, but faster than entrance. The
AI steps back with respect.

**Suggestions: directional arrival with stagger**
Classic dropdown: 200ms ease-out, instant dismiss.
Smart Window suggestions: grow downward from smartbar, 220ms AI settle
curve. Items stagger 25ms apart. Dismiss: 160ms fade (not instant — in
an AI context, instant disappearance feels like something broke).

**Chips: scale-from-origin with spatial continuity**
Classic: no chip behavior defined.
Smart Window: chips enter at 90%→100% scale with opacity, 240ms, 40ms
stagger. Follow-up chips that become user messages travel spatially
from source to destination (300ms). Conversation starters refresh with
a crossfade choreography (old out, beat, new in). Selection exit: scale
to 95% while fading, 150ms.

**Process transparency: replaces the spinner entirely**
Classic: no AI processing states.
Smart Window: expandable step-by-step process indicator. Collapsed shows
current step + progress bar. Expanded shows all steps with source names
appearing as found. Each step transition: 200ms crossfade. Progress bar
fills continuously. Source names stagger 30ms apart. The smartbar glow
fades as the process indicator appears — clean handoff from ambient
presence to active transparency.

**Response streaming: reading-speed word groups**
Classic: no streaming behavior.
Smart Window: text arrives in word groups at natural reading pace.
Markdown sections get a subtle settle (0.92→1.0 opacity, 200ms) when
complete. Action bar fades in 300ms after response finishes, icons
staggered 40ms — a beat after the AI finishes speaking.

**Error states: each failure type breaks the rhythm differently**
Classic: generic error styling.
Smart Window: model error = 100ms pause then 200ms fade. Rate limit =
rhythm completes its beat then 280ms settle. Content filtered = single
decisive 160ms beat. Network issue = browser-register timing (200ms)
because it's not the AI's fault. The motion tells you what happened
before you read the text.

**Tabs: warm flash on entering AI space**
Classic: expand in place, 200ms.
Smart Window: same expansion but with a brief warm acknowledgment —
the tab recognizes it's in the AI space. Tab drag between Smart↔Classic
transitions the visual warmth as the tab crosses the boundary.

**Kill switch: the emphasis moment**
Classic: no equivalent.
Smart Window: 500ms. AI presence (glow, gradient, warmth) recedes. The
lavender drains. Classic chrome settles. A beat of stillness before the
window finishes resolving. Reduced motion: instant switch with brief
opacity crossfade — same respect, no movement.

**Reduced motion: every deviation has a static equivalent**
Sidebar: instant expand, content crossfade. Suggestions: instant appear.
Chips: instant appear/disappear. Process: static indicators. Glow: static
at idle intensity. Kill switch: instant with crossfade. Information
always preserved. Warmth always preserved. Only movement removed.
