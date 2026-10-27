# math-pdf-builder

Turn Markdown notes full of LaTeX math into clean, styled PDF study guides, with a cover page, a clickable contents page, and coloured callout boxes for definitions, worked examples, tips and exam traps.

KaTeX is bundled in the repo, so math renders fully offline.

Sample output: [`examples/discrete-math.pdf`](examples/discrete-math.pdf)

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

## Usage

```bash
python mdpdf.py examples/discrete-math.md
python mdpdf.py notes.md -o guide.pdf -t "Linear Algebra" -s "Minor prep"
python mdpdf.py notes.md --html-only
```

The first `# Heading` becomes the cover title. Every `## Heading` goes into the contents page.

## Writing notes

Inline math goes in `$...$` and display math in `$$...$$`. Wrap a block in a callout like this:

```html
<div class="key-result" markdown="1">
**Euler's formula.** $v - e + f = 2$
</div>
```

Callout classes: `definition`, `key-result`, `formula-box`, `worked-example`, `tips`, `warning`, `exam-trap`.

## How it works

| Layer | Technology |
|-------|------------|
| Parsing | Python `markdown` (tables, fenced code, md-in-html) |
| Math | Math is pulled out before Markdown parsing so it can't get mangled, then rendered with KaTeX |
| Layout | HTML + CSS template (A4, print-styled) |
| PDF | Headless Chromium via Playwright |
