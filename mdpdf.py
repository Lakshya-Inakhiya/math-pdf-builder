#!/usr/bin/env python3
import argparse
import html
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "template.html"


def protect_math(md: str):
    store = []

    def keep(tex, display):
        store.append((tex, display))
        return f"@@MATH{len(store) - 1}@@"

    md = re.sub(r"(?s)\$\$(.+?)\$\$", lambda m: keep(m.group(1).strip(), True), md)
    md = re.sub(r"(?<![\\$])\$(?!\s)([^$\n]+?)(?<!\s)\$", lambda m: keep(m.group(1), False), md)
    return md, store


def restore_math(body: str, store):
    def put(m):
        tex, display = store[int(m.group(1))]
        tag, cls = ("div", "math block") if display else ("span", "math inline")
        return f'<{tag} class="{cls}">{html.escape(tex)}</{tag}>'

    body = re.sub(r"<p>@@MATH(\d+)@@</p>", put, body)
    return re.sub(r"@@MATH(\d+)@@", put, body)


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def build_html(md_text: str, title: str, subtitle: str) -> str:
    md_text, store = protect_math(md_text)
    body = markdown.markdown(md_text, extensions=["tables", "fenced_code", "md_in_html", "sane_lists"])
    body = restore_math(body, store)
    toc = []

    def anchor(m):
        text = re.sub(r"<[^>]+>", "", m.group(1))
        sid = slug(text)
        toc.append(f'<li><a href="#{sid}">{text}</a></li>')
        return f'<h2 id="{sid}">{m.group(1)}</h2>'

    body = re.sub(r"<h2>(.*?)</h2>", anchor, body)
    out = TEMPLATE.read_text(encoding="utf-8")
    for k, v in {"TITLE": html.escape(title), "SUBTITLE": html.escape(subtitle),
                 "KATEX": (ROOT / "katex").as_uri(),
                 "TOC": "<ol>" + "".join(toc) + "</ol>", "CONTENT": body}.items():
        out = out.replace("{{" + k + "}}", v)
    return out


def render_pdf(html_path: Path, pdf_path: Path):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(html_path.resolve().as_uri(), wait_until="networkidle")
        page.wait_for_function("window.__mathDone === true", timeout=30000)
        page.pdf(path=str(pdf_path), format="A4", print_background=True,
                 margin={"top": "16mm", "bottom": "18mm", "left": "15mm", "right": "15mm"})
        browser.close()


def main():
    ap = argparse.ArgumentParser(description="Markdown + LaTeX -> styled PDF study guide")
    ap.add_argument("input", type=Path)
    ap.add_argument("-o", "--output", type=Path)
    ap.add_argument("-t", "--title")
    ap.add_argument("-s", "--subtitle", default="Notes, definitions, worked examples and exam patterns.")
    ap.add_argument("--html-only", action="store_true")
    a = ap.parse_args()

    src = a.input.read_text(encoding="utf-8")
    m = re.match(r"#\s+(.+)\n", src)
    title = a.title or (m.group(1).strip() if m else a.input.stem)
    if m and not a.title:
        src = src[m.end():]
    out = a.output or a.input.with_suffix(".pdf")
    html_path = out.with_suffix(".html")
    html_path.write_text(build_html(src, title, a.subtitle), encoding="utf-8")
    if a.html_only:
        print(html_path)
        return
    render_pdf(html_path, out)
    html_path.unlink()
    print(out)


if __name__ == "__main__":
    main()
