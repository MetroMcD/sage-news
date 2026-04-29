---
name: sage-news-website-style
description: professional website and blog style guide for a sage news vibe-coding site. use when creating or reviewing website banners, blog article layouts, landing pages, content cards, css/html snippets, image prompts, or blog-ready reports for the sage news visual identity. emphasizes a modern light-blue/dark-blue editorial look with subtle playful cartoon energy, while enforcing a more professional blog-report variant without the phone hand or yellow logo rays.
---

# Sage News Website Style

## Purpose
Use this skill to create consistent website, banner, and blog assets for the `sage news` site. Keep the look modern, editorial, blue-forward, professional, and lightly playful. The visual direction may use friendly rounded illustration cues, but it must not copy a protected show, named franchise, character design, or exact art style.

## Core Brand Direction
- Positioning: professional ERP/news portal with approachable, lightweight gamification energy.
- Primary mood: clear, modern, confident, structured, readable.
- Visual language: flat 2D vector illustration, rounded geometry, clean outlines, soft gradients, editorial cards, modular UI blocks.
- Avoid: clutter, comic chaos, childish UI, exaggerated game overlays, direct references to protected franchises.

## Color System
Use these tokens as defaults:

```css
:root {
  --sn-blue-950: #061b49;
  --sn-blue-900: #082b6f;
  --sn-blue-800: #0a3b93;
  --sn-blue-600: #0d6ecf;
  --sn-blue-400: #38a9f5;
  --sn-blue-200: #bfe8ff;
  --sn-blue-100: #e8f7ff;
  --sn-white: #ffffff;
  --sn-ink: #07172f;
  --sn-muted: #5f728a;
  --sn-border: #d6e9f8;
  --sn-accent-yellow: #ffc82e;
}
```

Use yellow only as a restrained accent for buttons, badges, or small highlights. Do not use yellow as dominant blog-report decoration.

## Typography
Use a professional rounded sans-serif stack:

```css
font-family: Inter, Manrope, Nunito Sans, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
```

For hero/logo-style text, use bold rounded weights. For reports and article bodies, prioritize readability: 16-18 px body text, 1.55-1.7 line height, strong headings, short paragraphs.

## Website Banner Rules
For website banners and hero images:
- Keep `sage news` large and centered or slightly right of center.
- Use light-blue/dark-blue gradients, city/newsroom/cloud/dashboard motifs, and subtle editorial UI cards.
- A hand holding a smartphone may be used in general website hero/banner variants when it supports a dynamic news-app feeling.
- Avoid game-specific overlays such as levels, coins, XP bars, trophies, leaderboards, or achievement popups unless the user explicitly requests gamification.
- Use professional spacing and leave safe margins for responsive cropping.

### Safe Banner Image Prompt Template
Use this when asked to generate a new banner:

```text
Create a wide 16:9 website banner for "sage news". Modern light-blue and dark-blue palette, professional 2D vector illustration, rounded forms, clean bold outlines, soft gradients, subtle city/newsroom background, editorial website feeling, polished SaaS/news portal aesthetic, lightly playful but business-ready. Large readable text: "sage news". No copyrighted characters, no direct franchise imitation, no game UI overlays unless requested.
```

## Blog Report Variant
Use this stricter variant for reports/articles that will be published on the blog.

### Mandatory Visual Restrictions
For blog reports and professional article headers:
- Do not include the hand holding a phone.
- Do not include the yellow decorative strokes/rays next to the `sage news` logo.
- Do not include trophy, coin, level, XP, or other game UI elements.
- Avoid cartoon hands, character limbs, mascot-like elements, and exaggerated comic effects.
- Keep the layout calmer, more editorial, and more executive-ready than the homepage/banner variant.

### Blog Report Visual Direction
Use:
- Blue gradient header with subtle abstract arcs, grid lines, or soft newsroom/city silhouettes.
- Compact `sage news` logo treatment without yellow rays.
- Clean article cards, metadata chips, category labels, and structured information blocks.
- Optional subtle icons: document, bell, chart, calendar, database, ERP modules, dashboard widgets.
- White or very light panels over a blue background for readability.

### Blog Report Image Prompt Template
Use this when asked to create a blog header/report visual:

```text
Create a professional blog report header for "sage news" in a modern light-blue and dark-blue palette. Use a clean editorial SaaS/news portal look with subtle 2D vector city or dashboard elements, soft gradients, rounded cards, and high readability. Include the text "sage news" as a clean logo/title treatment. Do not include a hand with a phone. Do not include yellow decorative rays or strokes around the logo. Do not include trophies, coins, XP, levels, or game UI. Keep the tone professional, polished, and suitable for a business blog.
```

## Blog Content Rules
A blog article is primarily a short, professional summary and classification of a source. Preserve the source meaning, reduce complexity, and make the relevance for readers clear.

### Source Handling
- Treat the provided source as the primary authority. Do not add external claims unless the user explicitly asks for broader research.
- Summarize, do not reproduce. Avoid long verbatim passages and rewrite in original wording.
- If a source link is provided and the user wants it included, place it near the top or bottom as `Quelle: [Name der Quelle](URL)`.
- If the user is the source, state this transparently, e.g. `Quelle: eigene Analyse / internes Projektupdate von Rene Muenz`, without inventing an external link.
- If the source is unclear, mark the basis as `Quelle: vom Nutzer bereitgestellte Informationen` and avoid unsupported attribution.
- Always separate confirmed source content from interpretation or recommendation. Use phrases such as `Einordnung:` or `Aus Projektsicht bedeutet das:` for analysis.

### Editorial Standards
- Keep posts concise: usually 400-800 words unless the user asks for a longer deep dive.
- Start with the practical relevance, not with generic background.
- Use a precise, non-clickbait title. Prefer benefit, change, or implication over hype.
- Include a `Kurzfazit` with 2-3 sentences that can stand alone.
- Use short paragraphs, clear subheadings, and bullet lists only where they improve scanability.
- Write in professional DACH business German: calm, factual, implementation-oriented, no marketing exaggeration.
- Avoid emojis, forced jokes, exaggerated gamification wording, and sensational language.
- Define acronyms or niche terms briefly on first use if the audience may not know them.

### Required Content Checks
Before finalizing a blog article, verify:
- What exactly is the source?
- What is the one-sentence core message?
- Who is affected: Anwender, Admins, Consultants, Projektleitung, Management, Support?
- What changes operationally, technically, or commercially?
- What is confirmed by the source versus your own interpretation?
- Is there a concrete next step or recommendation?
- Are dates, product names, module names, versions, and links accurate as provided?

### Recommended Blog Structure
Use this structure by default and adapt only when the topic requires it:

```markdown
# [praeziser Titel]

**Kurzfazit:** [2-3 Saetze: Kernaussage, Relevanz, ggf. Handlungsbedarf]

**Quelle:** [Quelle / Link / eigene Analyse]

## Worum geht es?
[Sehr kurze Einordnung der Quelle und des Anlasses]

## Die wichtigsten Punkte
- [Punkt 1]
- [Punkt 2]
- [Punkt 3]

## Einordnung fuer die Praxis
[Was bedeutet das fuer Anwender, Projekte, Support oder Betrieb?]

## Empfehlung
[Konkreter naechster Schritt oder pragmatische Handlungsempfehlung]
```

### Optional Add-ons
Add these only when useful:
- `Fuer wen relevant?` for target audiences.
- `Auswirkungen auf Projekte` for implementation or rollout topics.
- `Risiken / offene Punkte` when the source leaves uncertainty.
- `Checkliste` for actionable operational posts.
- `Meta Description` with 140-160 characters for SEO snippets.
- `Alt-Text` for the blog header image, describing the visual neutrally and accessibly.

## Blog Report Writing Style
When drafting reports for the blog, write more professionally than a casual news post.

Default structure:

```markdown
# [praegnanter Titel]

**Kurzfazit:** [2-3 Saetze mit Ergebnis und Relevanz]

## Ausgangslage
[Kontext, Problem, Anlass]

## Was ist neu / was wurde beobachtet?
[Konkrete Punkte, faktenorientiert]

## Bedeutung fuer Anwender und Projekte
[Auswirkungen, Chancen, Risiken]

## Empfehlung / naechster Schritt
[Konkrete Handlungsempfehlung]
```

Tone:
- Professional DACH business German.
- Direct, precise, implementation-oriented.
- Avoid hype, jokes, excessive emojis, and over-gamified wording.
- Use short paragraphs and clear subheadings.
- Distinguish facts from assumptions.

## HTML/CSS Starter Pattern
Use this as a baseline for website or blog sections:

```html
<section class="sn-hero sn-hero--report">
  <div class="sn-hero__content">
    <p class="sn-eyebrow">sage news</p>
    <h1>Aktuelle ERP- und Projekteinblicke</h1>
    <p class="sn-lead">Kompakte Updates, fachlich eingeordnet und praxisnah aufbereitet.</p>
  </div>
</section>
```

```css
.sn-hero {
  background: radial-gradient(circle at 20% 20%, var(--sn-blue-200), transparent 32%),
              linear-gradient(135deg, var(--sn-blue-950), var(--sn-blue-600));
  border-radius: 28px;
  color: var(--sn-white);
  padding: clamp(32px, 6vw, 72px);
  overflow: hidden;
}

.sn-hero--report {
  min-height: 280px;
}

.sn-eyebrow {
  display: inline-flex;
  padding: 6px 12px;
  border: 1px solid rgba(255,255,255,.28);
  border-radius: 999px;
  background: rgba(255,255,255,.12);
  font-weight: 700;
  letter-spacing: .04em;
  text-transform: uppercase;
}

.sn-lead {
  max-width: 720px;
  color: rgba(255,255,255,.86);
  font-size: clamp(1rem, 1.4vw, 1.25rem);
  line-height: 1.65;
}
```

## Quality Checklist
Before delivering any output, verify:
- The intended variant is clear: banner/general website or blog-report.
- Blog reports contain no phone hand and no yellow logo rays.
- The output is professional enough for a business website.
- The text `sage news` is spelled exactly unless the user asks otherwise.
- Color usage stays within the blue-forward palette.
- Any playful elements are subtle and not game-heavy.
- Blog articles summarize a clear source, distinguish facts from interpretation, and provide a practical recommendation.
