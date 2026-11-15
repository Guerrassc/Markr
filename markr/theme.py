import html

STATUS_TEXT = {"met": "Met", "missing": "Missing", "uncertain": "Uncertain"}

CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap');

:root {
  --ink: #1c1c1c;
  --muted: #6b665d;
  --line: #e3ddd2;
  --paper: #faf8f4;
  --accent: #1f2a44;
  --gold: #b08d4a;
  --met: #2f6b4f;
  --missing: #9b3b35;
  --uncertain: #8a6d1f;
}

.stApp { background: var(--paper); color: var(--ink); font-family: 'Inter', -apple-system, 'Segoe UI', Roboto, sans-serif; }
header[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 760px; padding-top: 3.5rem; padding-bottom: 5rem; }
.stApp textarea, .stApp button, .stApp input { font-family: 'Inter', -apple-system, 'Segoe UI', Roboto, sans-serif !important; }
.stButton > button { border-radius: 2px; font-weight: 500; padding: 0.55rem 1.5rem; }

.mk-brand { font-family: 'Source Serif 4', Georgia, serif; font-size: 3.2rem; font-weight: 600; letter-spacing: -0.03em; line-height: 1.05; color: var(--ink); }
.mk-brand::after { content: ""; display: block; width: 48px; height: 3px; background: var(--gold); margin-top: 0.9rem; }
.mk-tagline { color: var(--muted); font-size: 1.05rem; margin: 1.1rem 0 1.6rem; line-height: 1.5; }
.mk-note { border-left: 3px solid var(--gold); background: #f3eee4; padding: 0.85rem 1.1rem; color: var(--muted); font-size: 0.88rem; line-height: 1.55; margin-bottom: 3rem; }

.mk-eyebrow { text-transform: uppercase; letter-spacing: 0.14em; font-size: 0.72rem; font-weight: 600; color: var(--muted); margin-top: 2.5rem; }
.mk-h2 { font-family: 'Source Serif 4', Georgia, serif; font-size: 1.7rem; font-weight: 600; letter-spacing: -0.01em; margin: 0.2rem 0 1rem; color: var(--ink); }
.mk-sub { font-family: 'Source Serif 4', Georgia, serif; font-size: 1.2rem; font-weight: 600; margin: 2rem 0 0.6rem; color: var(--ink); }
.mk-small { color: var(--muted); font-size: 0.85rem; margin: 0.4rem 0 0.8rem; }

.mk-list { margin: 0.5rem 0 1rem; }
.mk-row { border-top: 1px solid var(--line); padding: 1.1rem 0 1.2rem; }
.mk-row:last-child { border-bottom: 1px solid var(--line); }
.mk-status { display: inline-block; font-size: 0.68rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; padding: 0.18rem 0.55rem; border: 1px solid currentColor; border-radius: 2px; margin-bottom: 0.5rem; }
.mk-req { font-weight: 500; font-size: 1rem; line-height: 1.45; margin: 0 0 0.55rem; color: var(--ink); }
.mk-quote { border-left: 2px solid var(--line); padding-left: 0.85rem; color: var(--muted); font-size: 0.87rem; line-height: 1.55; margin: 0.4rem 0; }
.mk-quote b { display: block; font-weight: 600; font-size: 0.66rem; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.1rem; }
.mk-hint { color: var(--muted); font-size: 0.82rem; font-style: italic; margin-top: 0.4rem; }

.mk-stats { display: flex; flex-wrap: wrap; gap: 2.2rem; padding: 1.3rem 0; border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); margin: 0.5rem 0 1.4rem; }
.mk-stat-n { font-family: 'Source Serif 4', Georgia, serif; font-size: 2.1rem; font-weight: 600; line-height: 1; color: var(--ink); }
.mk-stat-l { font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.12em; color: var(--muted); margin-top: 0.35rem; }

.mk-met { color: var(--met); }
.mk-missing { color: var(--missing); }
.mk-uncertain { color: var(--uncertain); }
</style>"""


def esc(text):
    clean = " ".join(str(text or "").split())
    return html.escape(clean).replace("$", "&#36;")


def section(number, title):
    return f'<div class="mk-eyebrow">Step {number}</div><div class="mk-h2">{esc(title)}</div>'


def requirement_row(req, status=None, evidence="", note=""):
    parts = ['<div class="mk-row">']
    if status in STATUS_TEXT:
        parts.append(f'<span class="mk-status mk-{status}">{STATUS_TEXT[status]}</span>')
    parts.append(f'<div class="mk-req">{esc(req["requirement"])}</div>')
    parts.append(f'<div class="mk-quote"><b>In the brief</b>{esc(req["source_quote"])}</div>')
    if evidence:
        parts.append(f'<div class="mk-quote"><b>In your draft</b>{esc(evidence)}</div>')
    if note:
        parts.append(f'<div class="mk-hint">{esc(note)}</div>')
    parts.append("</div>")
    return "".join(parts)


def stats_html(words, pages, counts):
    items = [(words, "Words", "")]
    if pages:
        items.append((pages, "Pages", ""))
    items += [(counts["met"], "Met", "met"),
              (counts["missing"], "Missing", "missing"),
              (counts["uncertain"], "Uncertain", "uncertain")]
    cells = ""
    for n, label, cls in items:
        color = f" mk-{cls}" if cls else ""
        cells += f'<div><div class="mk-stat-n{color}">{n}</div><div class="mk-stat-l">{label}</div></div>'
    return f'<div class="mk-stats">{cells}</div>'