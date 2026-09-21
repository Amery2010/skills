---
name: frontend-ui-aesthetics
description: Design and implement art-directed, visually ambitious websites with expressive typography and purposeful motion. Use for cinematic landing pages, creative portfolios, editorial or campaign sites, immersive experiences, and high-impact visual redesigns. Use for dashboards or utility interfaces only when the user explicitly requests an experimental treatment.
---

# Frontend UI Aesthetics

Create a recognizable visual concept that serves the site's audience and primary action. Treat standout Awwwards, FWA, and CSS Design Awards work as a craft benchmark, not a promise of recognition. Match the intervention to the request: a section-level improvement does not require a site-wide redesign.

## Establish the Direction

Inspect the existing framework, routes, components, content, assets, and design conventions before choosing a direction. For a redesign, inspect the rendered experience when browser access is available and identify which behaviors and visual cues must survive.

State a compact brief: audience, purpose, primary action, one-sentence visual thesis, and the few design principles that distinguish this project. Infer these from the supplied material when possible; clarify only missing decisions that would change the implementation. Follow a supplied brand or reference direction rather than inventing a competing concept.

Define completion in observable terms: required routes and interactions still work, the main composition fits representative viewports, content remains readable, and motion has an accessible fallback. This brief guides implementation; it is not an approval checkpoint unless the user asks for one.

## Preserve the Product Contract

- Retain the project's framework, public URLs, data flows, form behavior, selectors used by consumers, and accessible names unless the requested change requires an update. Keep unrelated changes out of the diff.
- Reuse the existing design system and components where they support the direction. Extend tokens deliberately instead of layering competing style systems.
- Use Lucide for functional interface icons, with consistent size, stroke, alignment, and states. Keep brand marks and bespoke illustration as artwork. Scope icon replacement to the surfaces being changed; a local edit is not a reason to migrate every icon.
- Keep visible interface copy and decoration free of emoji. Preserve user-authored content and externally supplied data rather than filtering or rewriting them to enforce this design preference.
- Every control must have a real destination or behavior. Represent unavailable integrations honestly; use verified assets or explicit placeholders rather than fabricated URLs or invented product claims.

## Art Direction

Choose one coherent concept and apply it through these decisions:

| Dimension | Decision to make | Check against |
| --- | --- | --- |
| Composition | Hierarchy, asymmetry, negative space, selective overlap, section rhythm | The primary action stays discoverable; every section has a distinct purpose |
| Typography | Expressive display face, readable body face, deliberate scale and line breaks | Real content, long titles, target languages, available font assets, and small screens |
| Color and material | Focused palette with semantic roles; texture or effects that support the concept | Text and control contrast, clear focus and error states |
| Imagery | One consistent treatment for provided, licensed, or generated assets | Asset availability, visual coherence, loading cost, useful alternative text |
| Motion | Timing, easing, and transitions tied to user intent | Immediate input feedback, reduced motion, touch input, and rendering fallback |

Use unconventional composition where it improves hierarchy or narrative. Avoid interchangeable card grids, generic startup copy, and decorative effects with no role in the concept. Familiar layouts are appropriate when they serve the content; originality must come from deliberate decisions rather than arbitrary novelty.

For canvas, WebGL, video, parallax, or kinetic typography, keep essential content and actions available through semantic DOM or an equivalent usable fallback. Prefer transform and opacity for motion where practical. Preserve native scrolling and avoid effects that obstruct input. Respect `prefers-reduced-motion` with a calm, fully usable experience.

## Implement and Verify

1. Establish or extend tokens for type, color, spacing, layers, and motion. Build semantic structure and the main responsive composition using real content.
2. Implement the strongest visual moment first, then extend the same system through the requested surfaces. Add motion after layout and content are stable.
3. Complete relevant hover, focus, active, loading, empty, error, and disabled states. Ensure keyboard and touch users can reach actions that appear on hover.
4. Run relevant project checks within the task's permissions. Remove unused code, dependencies, and effects introduced by this work.
5. Inspect the real page at representative mobile, tablet, and desktop sizes, plus content-driven breakpoints. Check navigation, forms, focus order, reduced motion, long content, overflow, clipping, layout shifts, and obstruction by sticky or layered elements.

Use browser inspection when available and permitted. Do not interpret this workflow as permission to run E2E suites or install browser tooling. If browser access or another check is unavailable, finish feasible checks and identify the unverified behavior; source inspection alone does not establish visual quality. Stop preview services started for the task when finished.

## Handoff

Report the visual thesis, the main changes, checks actually performed (including viewport sizes when inspected), and remaining limitations. Distinguish implemented fallbacks from fallbacks actually exercised. Keep the result proportional to the scope of the change.
