# Design System — Anuroop Sriram

## Product context

This is the canonical professional site for Anuroop Sriram, an AI-for-Science
researcher and research leader. It serves research peers, collaborators,
technical leaders, journalists, students, search engines, and citation agents.

The memorable first impression is: **a visionary researcher building the
intelligence layer for science and engineering, with the record to support it.**

## Visual thesis

**Scientific instrument meets editorial monograph.** The site combines the
precision and luminosity of a research instrument with the calm authority of a
well-edited scientific publication. One data-driven GPU field may be expressive;
the rest of the interface should be restrained, legible, and evidence-led.

Avoid generic SaaS card grids, purple gradients, bubbly surfaces, decorative
icons, hidden navigation, and motion without narrative purpose.

## Typography

- Display: **Newsreader Variable**, with optical sizing enabled.
- Body and UI: **Instrument Sans Variable**.
- Metadata and technical labels: **Spline Sans Mono Variable**.
- Body copy never drops below 1rem. Long-form measure is 62–72 characters.
- Headings use tight line-height and balanced wrapping; body text uses pretty
  wrapping and generous leading.

## Color

Colors are defined in OKLCH and switch through `light-dark()`.

- Paper: warm, quiet, and slightly mineral rather than pure white.
- Ink: green-black rather than neutral black.
- Raised/inset surfaces: tonal steps, not floating gray cards.
- Spectral cyan: primary action and live-system signal.
- Amber: rare emphasis for impact, chronology, and energy.
- Borders are hairlines. Shadows are used only when depth communicates state.

Dark mode is a full surface redesign, not an inversion. Accents lose saturation
and text remains warm to avoid a neon-on-black developer-portfolio aesthetic.

## Layout

- Wide composition: up to 90rem for the home poster and 76rem for indexes.
- Reading measure: 68ch.
- Grid: 12 columns on wide screens, 6 on tablets, and 4 on mobile.
- Components adapt through container queries before page breakpoints.
- Cards exist only when the whole surface is an interaction. Lists and research
  records use editorial rows and rules.

## Motion

- Motion has three jobs: establish the research field, preserve orientation
  between pages, and reveal hierarchy while scrolling.
- Primary easing: `cubic-bezier(.22, 1, .36, 1)`.
- Micro interactions: 120–220ms. Compositional transitions: 450–800ms.
- Scroll-linked motion is limited to the hero/research-atlas sequence.
- Reduced-motion, Save-Data, hidden-tab, offscreen, and low-power paths are
  first-class designs.

## GPU experience

The Research Field visualizes real publication and dataset metadata. It never
renders essential text or controls. Runtime ladder:

1. WebGPU/WGSL
2. WebGL2/GLSL
3. deterministic SVG/CSS still

The renderer starts after textual first paint, pauses offscreen, adapts DPR and
frame rate, and recovers from device/context loss without layout shift.

## Interaction and accessibility

- Every action has visible text or an accessible name.
- Keyboard focus is high contrast and never removed.
- Touch targets are at least 44×44 CSS pixels.
- Body contrast meets WCAG AA; text is never placed directly on a busy field.
- Native HTML (`article`, `search`, `details`, `time`, `dialog`/popover) is the
  baseline. Advanced CSS and GPU features are progressive enhancement.
- Links remain visibly links and visited links remain distinguishable.

## Content hierarchy

1. Who Anuroop is and what he is building now.
2. Independent evidence of impact.
3. The research arc and landmark work.
4. Publications, datasets, and current activity.
5. Clear routes to cite, follow, or contact.

Claims must be dated where they can change and linked to authoritative sources.
No metric or accomplishment is introduced without verification.
