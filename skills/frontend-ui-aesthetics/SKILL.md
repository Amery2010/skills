---
name: frontend-ui-aesthetics
description: Design and implement visually ambitious, production-ready marketing, portfolio, editorial, campaign, and immersive websites with strong art direction, experimental typography, refined motion, and premium interaction quality. Use when the user requests an Awwwards-level frontend, a cinematic or unconventional website, an immersive landing page, a creative portfolio, or a high-impact visual redesign. Do not use for routine dashboards or utility interfaces unless the user explicitly requests an experimental treatment.
---

# Frontend UI Aesthetics

## Objective

Create a cohesive digital experience that treats the browser as an interactive, art-directed canvas.

Aim for the craft and originality associated with standout Awwwards, FWA, and CSS Design Awards projects. Treat these references as a quality benchmark, never as a guarantee of recognition. Preserve usability, accessibility, performance, and the website's core purpose.

## Establish the Direction

Before implementation:

1. Inspect the existing project, content, assets, framework, and constraints.
2. State any important assumptions that cannot be verified.
3. Define the website's audience, purpose, desired emotion, and primary action.
4. Write a one-sentence visual thesis that gives the experience a distinct point of view.
5. Select three to five design principles that govern typography, composition, imagery, color, and motion.
6. Define verifiable completion criteria for responsive behavior, interactions, accessibility, and runtime quality.

Choose one strong creative concept and execute it consistently. Do not combine unrelated visual trends or effects.

## Non-Negotiable Rules

- Use Lucide for all functional interface icons.
- Keep icon size, stroke weight, alignment, and interaction states consistent.
- Never use emojis in visible interface copy, navigation, controls, decoration, bullets, placeholders, or status indicators.
- Reserve custom SVG artwork for logos, brand marks, and bespoke illustrations that Lucide cannot represent.
- Preserve the project's existing framework and conventions unless the request requires a change.
- Touch only the code necessary to deliver the requested experience.
- Keep every interaction functional. Do not create decorative controls, fake buttons, or unfinished states.
- Do not invent remote asset URLs or present unavailable integrations as working.
- Avoid generic template aesthetics and interchangeable AI-generated layouts.

## Art Direction

### Composition

- Use the viewport as a spatial composition rather than a stack of conventional content blocks.
- Explore asymmetry, controlled overlap, cropped elements, layered depth, unexpected alignment, and deliberate negative space.
- Break the grid only when doing so strengthens hierarchy or narrative.
- Keep unconventional layouts understandable, navigable, and responsive.
- Give every section a clear role in the visual and informational sequence.

### Typography

- Treat typography as a primary visual material.
- Build a deliberate scale with expressive display type and highly readable body type.
- Use contrast in scale, weight, width, rhythm, and alignment to create impact.
- Apply experimental line breaks and kinetic type intentionally.
- Preserve legibility across languages, screen sizes, and content lengths.
- Avoid default-looking type systems and arbitrary oversized headings.

### Color and Material

- Use a focused palette with clear semantic and emotional intent.
- Maintain sufficient text and control contrast.
- Use gradients, glow, blur, glass effects, grain, and texture only when they belong to the concept.
- Avoid decorative effects that compete with content or obscure interaction states.

### Imagery and Rendering

- Combine photography, illustration, procedural graphics, video, canvas, WebGL, or generated assets only when they support one coherent art direction.
- Prefer high-quality, correctly licensed, provided, or generated assets.
- Optimize images, textures, video, and 3D resources for web delivery.
- Provide meaningful fallbacks when advanced rendering is unavailable.
- Never use visual complexity merely to demonstrate technical capability.

## Interaction and Motion

- Design motion as a system with consistent timing, easing, momentum, and hierarchy.
- Use physical qualities such as inertia, spring, friction, parallax, or magnetic response when they reinforce the concept.
- Connect transitions to user intent and spatial relationships.
- Prioritize transform and opacity animations where practical.
- Keep input feedback immediate and animation smooth.
- Avoid excessive cursor effects, perpetual motion, scroll-jacking, and ornamental animation.
- Respect `prefers-reduced-motion` and provide a calm equivalent experience.
- Ensure essential content and actions remain available without animation or advanced rendering.

## Avoid Generic Design Patterns

Do not default to:

- A centered headline over gradient blobs
- Repetitive rounded cards
- Arbitrary glassmorphism
- Excessive pill-shaped controls
- Random floating objects
- Uniform section spacing without narrative rhythm
- Decorative dashboards or metrics unrelated to the content
- Generic startup copy
- Effects copied from references without adapting them to the project

Remove any element that lacks a clear visual, narrative, or functional purpose.

## Implementation Workflow

1. Audit the current experience and preserve all required behavior.
2. Establish tokens for typography, color, spacing, layers, motion, and responsive behavior.
3. Implement semantic structure and the main responsive composition.
4. Build the strongest visual moment first to validate the art direction.
5. Extend the same system across the remaining sections.
6. Add motion progressively after layout and content are stable.
7. Polish hover, focus, active, loading, empty, and error states.
8. Remove unnecessary abstractions, dependencies, effects, and unused code introduced by the work.
9. Run the project's relevant static checks and tests.
10. Inspect the real page in a browser at representative mobile, tablet, and desktop sizes.

## Quality Gate

Do not consider the work complete until:

- The page communicates a recognizable visual concept.
- Every major design decision supports that concept.
- Typography is expressive without compromising readability.
- Lucide is used consistently for functional icons.
- No emoji appears anywhere in the visible interface.
- Navigation and interactive elements work with keyboard and pointer input.
- Focus states are visible.
- Semantic landmarks, labels, alternative text, and contrast are appropriate.
- Reduced-motion behavior is implemented.
- Mobile and desktop layouts both feel intentionally composed.
- No unintended overflow, clipping, layout shift, or interaction obstruction remains.
- Assets are optimized and advanced effects degrade gracefully.
- The implemented result has been inspected in the browser rather than judged from source code alone.
- Any remaining limitation is reported explicitly instead of being hidden.

## Handoff

Summarize:

- The visual thesis
- The main implementation decisions
- The checks and viewport sizes verified
- Any remaining constraints or unavailable capabilities
