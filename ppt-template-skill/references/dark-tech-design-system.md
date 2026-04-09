# Dark Tech Design System

## Scope

This reference captures the presentation language extracted from the Mimo/OpenClaw demo video and turns it into reusable PPT construction rules.

## Core Look

- Background: near-black with a slight blue or violet cast, typically `#0D0D12` or `#000000`
- Tone: hard contrast, low clutter, large titles, neon-accent highlights
- Mood: product demo, AI tooling, code walkthrough, future-tech announcement

## Canvas

- Ratio: 16:9
- Working size: `1920x1080`
- Margins: `50px`
- Footer band: reserve about `30-50px`
- Card gap: `20px`
- Card radius: `8-16px`

## Typography

- H1: bold sans-serif, `56-84pt`, center or upper-center
- H2: bold sans-serif, `28-36pt`
- Body: regular sans-serif, `18-24pt`
- Code: monospace, `14-18pt`
- Recommended fonts:
  - `Microsoft YaHei`
  - `Source Han Sans`
  - `Consolas` for code

## Color System

- Base background: `#0D0D12`
- Primary text: `#FFFFFF`
- Secondary text: `#CCCCCC`
- Quiet text: `#8A92A6`
- Accent cyan: `#00F0FF`
- Accent purple: `#D4A0FF`
- Accent orange: `#FF9A00`
- Accent green: `#00FF88`
- Accent red: `#FF4444`

## Graphic Language

- Cards use dark fills, light borders, and rounded corners
- Borders are thin and low-contrast, around `20-40%` transparency
- Use glow through large blurred color orbs in the background, not through heavy drop shadows
- Avoid thick dividers and noisy iconography
- Screenshot containers should feel like dark device frames or dark social cards

## Slide Taxonomy

### 1. Cover / Key Concept

- Very large central title
- Small brand label above
- One concise subtitle
- Strong glow behind the title

### 2. Evidence / Quote

- One large centered card
- Small supporting title at top
- Use for tweet screenshots, article evidence, or external proof

### 3. Comparison

- Two symmetric columns
- Left and right should differ by title color or accent chips
- Use one hard contrast per slide

### 4. Data / Leaderboard

- Dark chart card
- One highlighted bar or metric
- Supporting callout sentence under the chart

### 5. Code / CLI

- Large code window
- Separate explanation panel
- Show command, config, or markdown snippets

### 6. CTA / Ending

- Big closing statement
- One action card
- One repo or contact block

## Editing Rules

- Keep one thesis per slide
- Limit each slide to one dominant visual pattern
- Highlight only one or two key phrases with accent colors
- Prefer large blocks and strong spacing over dense bullet lists
- If screenshots are inserted later, place them inside existing dark rounded containers rather than edge-to-edge

## Rebuild Checklist

1. Confirm the deck uses only one background family.
2. Confirm all titles are visibly larger than body text by at least one strong step.
3. Confirm accent colors are sparse and intentional.
4. Confirm cards align to the same horizontal rhythm.
5. Confirm the deck remains editable without replacing the entire layout.
