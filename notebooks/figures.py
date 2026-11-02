"""Functions that draw the paper's tables and figures as SVG (white background, Helvetica,
category names in a monospaced font, white-to-#3b6fb6 color ramp).

The PDFs used in the paper are rendered from these SVGs with `rsvg-convert -f pdf`.
"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd

BLUE = (0x3B, 0x6F, 0xB6)
STRIPE = "#f4f6f9"
MONO = "Menlo, Consolas, monospace"


def color(v, vmax):
    t = min(max(v / vmax, 0), 1)
    return "#%02x%02x%02x" % tuple(round(255 + (BLUE[i] - 255) * t) for i in range(3))


def esc(s):
    return str(s).replace("&", "&amp;")


def save(svg, path):
    """Writes the SVG and, if rsvg-convert is installed, also the PDF."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg, encoding="utf-8")
    if shutil.which("rsvg-convert"):
        subprocess.run(["rsvg-convert", "-f", "pdf", "-o", str(path.with_suffix(".pdf")), str(path)], check=True)
    print("saved", path)


def svg_formats_table(table):
    """Formats table. `table`: columns format, tool, files, pct (with the Total row)."""
    W, rh, T = 640, 30, 60
    H = T + rh * len(table) + 20
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'font-family="Helvetica, Arial, sans-serif">', '<rect width="100%" height="100%" fill="#fff"/>',
         '<line x1="16" x2="624" y1="20" y2="20" stroke="#111" stroke-width="1.6"/>',
         '<text x="24" y="45" font-size="14" font-weight="700" fill="#111">Context file</text>',
         '<text x="270" y="45" font-size="14" font-weight="700" fill="#111">Tool</text>',
         '<text x="480" y="45" font-size="14" font-weight="700" fill="#111" text-anchor="end">Files</text>',
         '<text x="610" y="45" font-size="14" font-weight="700" fill="#111" text-anchor="end">Share (%)</text>',
         '<line x1="16" x2="624" y1="60" y2="60" stroke="#111" stroke-width="0.9"/>']
    for i, r in enumerate(table.itertuples()):
        y = T + i * rh
        total = r.format == "Total"
        if total:
            o.append(f'<line x1="16" x2="624" y1="{y}" y2="{y}" stroke="#111" stroke-width="0.9"/>')
        elif i % 2:
            o.append(f'<rect x="16" y="{y}" width="608" height="{rh}" fill="{STRIPE}"/>')
        weight = ' font-weight="700"' if total else ""
        font = "" if total else f' font-family="{MONO}"'
        o.append(f'<text x="24" y="{y + 20}" font-size="14"{font}{weight} fill="#111">{esc(r.format)}</text>'
                 f'<text x="270" y="{y + 20}" font-size="14" fill="#111">{esc(r.tool)}</text>'
                 f'<text x="480" y="{y + 20}" font-size="14"{weight} fill="#111" text-anchor="end">{r.files:,}</text>'
                 f'<text x="610" y="{y + 20}" font-size="14"{weight} fill="#111" text-anchor="end">{r.pct:.2f}</text>')
    yb = T + rh * len(table)
    o.append(f'<line x1="16" x2="624" y1="{yb}" y2="{yb}" stroke="#111" stroke-width="1.6"/></svg>')
    return "\n".join(o)


def svg_categories_table(prev, n_files):
    """Prevalence table. `prev`: columns category, files, pct (sorted)."""
    W, rh, T = 640, 30, 60
    H = T + rh * len(prev) + 32 + 20
    scale = 1.857  # px per percentage point
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'font-family="Helvetica, Arial, sans-serif">', '<rect width="100%" height="100%" fill="#fff"/>',
         '<line x1="16" x2="624" y1="20" y2="20" stroke="#111" stroke-width="1.6"/>',
         '<text x="24" y="45.0" font-size="14" font-weight="700" fill="#111" text-anchor="start">Category</text>',
         '<text x="400" y="45.0" font-size="14" font-weight="700" fill="#111" text-anchor="end">Files</text>',
         '<text x="430" y="45.0" font-size="14" font-weight="700" fill="#111" text-anchor="start">Share (%)</text>',
         '<line x1="16" x2="624" y1="60" y2="60" stroke="#111" stroke-width="0.9"/>']
    for i, r in enumerate(prev.itertuples()):
        y = T + i * rh
        if i % 2:
            o.append(f'<rect x="16" y="{y}" width="608" height="{rh}" fill="{STRIPE}"/>')
        w = r.pct * scale
        o.append(f'<text x="24" y="{y + 20:.1f}" font-size="14" font-family="{MONO}" fill="#111">{esc(r.category)}</text>'
                 f'<text x="400" y="{y + 20:.1f}" font-size="14" fill="#111" text-anchor="end">{r.files:,}</text>'
                 f'<rect x="430" y="{y + 9:.1f}" width="{w:.1f}" height="12" rx="2" fill="#3b6fb6"/>'
                 f'<text x="{430 + w + 8:.1f}" y="{y + 20:.1f}" font-size="14" fill="#111">{r.pct:.1f}</text>')
    yb = T + rh * len(prev)
    o.append(f'<line x1="16" x2="624" y1="{yb}" y2="{yb}" stroke="#111" stroke-width="1.6"/>')
    o.append(f'<text x="624" y="{yb + 16}" font-size="11" fill="#555" text-anchor="end">N = {n_files:,} files; '
             f'multi-label, so shares do not sum to 100%.</text>')
    o.append("</svg>")
    return "\n".join(o)


def svg_jaccard_column(jac, names, c=25, left=92, base=78):
    """Jaccard matrix (lower triangle, no diagonal) at the width of one column."""
    names = [esc(s) for s in names]
    n = len(names)
    W, H = left + (n - 1) * c + 4, (n - 1) * c + base
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'font-family="Helvetica, Arial, sans-serif"><rect width="{W}" height="{H}" fill="#fff"/>']
    for i in range(1, n):
        y = (i - 1) * c
        o.append(f'<text x="{left - 5}" y="{y + c / 2 + 3.5:.1f}" font-size="10" text-anchor="end" fill="#111">{names[i]}</text>')
        for j in range(i):
            v = jac[i, j]
            x = left + j * c
            o.append(f'<rect x="{x}" y="{y}" width="{c}" height="{c}" fill="{color(v, 0.8)}" stroke="#fff" stroke-width="1"/>'
                     f'<text x="{x + c / 2:.1f}" y="{y + c / 2 + 3:.1f}" font-size="8.5" text-anchor="middle" '
                     f'fill="{"#fff" if v / 0.8 > 0.5 else "#111"}">{v:.2f}'.replace(">0.", ">.") + '</text>')
    yb = (n - 1) * c + 5
    for j in range(n - 1):
        x = left + j * c + c / 2 + 3
        o.append(f'<text transform="translate({x:.1f},{yb}) rotate(-50)" font-size="10" text-anchor="end" fill="#111">{names[j]}</text>')
    o.append("</svg>")
    return "".join(o)


def svg_size(n_categories, characters):
    """Boxplot of the size (log) by number of categories. Returns (svg, table of medians)."""
    d = pd.DataFrame({"k": n_categories, "lg": np.log10(np.clip(characters, 1, None))})
    W, H, xl, xr, yt, yb = 640, 380, 78, 620, 44, 300
    ks = sorted(d["k"].unique())
    step = (xr - xl - 44) / (len(ks) - 1)
    ypos = lambda lg: yb - lg / 5 * (yb - yt)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'font-family="Helvetica, Arial, sans-serif">', '<rect width="100%" height="100%" fill="#fff"/>',
         '<line x1="16" x2="624" y1="20" y2="20" stroke="#111" stroke-width="1.6"/>']
    for i in range(1, len(ks), 2):
        x = xl + 22 + i * step
        o.append(f'<rect x="{x - step / 2:.1f}" y="{yt}" width="{step:.1f}" height="{yb - yt}" fill="{STRIPE}"/>')
    for e in range(6):
        y = ypos(e)
        o.append(f'<line x1="{xl}" x2="{xr}" y1="{y:.1f}" y2="{y:.1f}" stroke="#e3e7ee"/>'
                 f'<text x="70" y="{y + 4:.1f}" font-size="12" fill="#444" text-anchor="end">{10 ** e:,}</text>')
    rows = []
    for i, kk in enumerate(ks):
        x = xl + 22 + i * step
        v = d.loc[d["k"] == kk, "lg"].values
        q1, med, q3 = np.percentile(v, [25, 50, 75])
        iqr = q3 - q1
        lo, hi = v[v >= q1 - 1.5 * iqr].min(), v[v <= q3 + 1.5 * iqr].max()
        for f in v[(v < lo) | (v > hi)]:
            o.append(f'<circle cx="{x:.1f}" cy="{ypos(f):.1f}" r="2.2" fill="none" stroke="#555" stroke-width="0.8"/>')
        o.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{ypos(hi):.1f}" y2="{ypos(q3):.1f}" stroke="#111" stroke-width="1"/>'
                 f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{ypos(q1):.1f}" y2="{ypos(lo):.1f}" stroke="#111" stroke-width="1"/>'
                 f'<line x1="{x - 6:.1f}" x2="{x + 6:.1f}" y1="{ypos(lo):.1f}" y2="{ypos(lo):.1f}" stroke="#111" stroke-width="1"/>'
                 f'<line x1="{x - 6:.1f}" x2="{x + 6:.1f}" y1="{ypos(hi):.1f}" y2="{ypos(hi):.1f}" stroke="#111" stroke-width="1"/>'
                 f'<rect x="{x - 11:.1f}" y="{ypos(q3):.1f}" width="22" height="{ypos(q1) - ypos(q3):.1f}" rx="2" fill="#3b6fb6"/>'
                 f'<line x1="{x - 11:.1f}" x2="{x + 11:.1f}" y1="{ypos(med):.1f}" y2="{ypos(med):.1f}" stroke="#fff" stroke-width="2"/>'
                 f'<text x="{x:.1f}" y="320" font-size="13" fill="#111" text-anchor="middle" font-weight="700">{kk}</text>'
                 f'<text x="{x:.1f}" y="337" font-size="11" fill="#555" text-anchor="middle">n={len(v)}</text>')
        rows.append({"n_categories": kk, "files": len(v), "median_characters": round(10 ** med)})
    o.append(f'<line x1="{xl}" x2="{xr}" y1="{yb}" y2="{yb}" stroke="#111" stroke-width="0.9"/>'
             f'<text x="{(xl + xr) / 2}" y="358" font-size="14" font-weight="700" fill="#111" text-anchor="middle">Number of categories in the file</text>'
             f'<text transform="translate(22,{(yt + yb) / 2}) rotate(-90)" font-size="14" font-weight="700" fill="#111" text-anchor="middle">File size (characters, log scale)</text>'
             '<line x1="16" x2="624" y1="366" y2="366" stroke="#111" stroke-width="1.6"/></svg>')
    return "\n".join(o), pd.DataFrame(rows)


def svg_format_category(summary, n_per_format, formats, labels, omitted, alpha=0.05):
    """Format × category table (% of files), with Cramér's V and † for p >= alpha."""
    L, cw0, cw, vw, rh, T = 24, 272, 110, 70, 30, 96
    ncol = len(formats)
    W, H = L + cw0 + cw * ncol + vw + 24, T + rh * len(summary) + 58
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'font-family="Helvetica, Arial, sans-serif"><rect width="{W}" height="{H}" fill="#fff"/>',
         f'<text x="{L}" y="24" font-size="15" font-weight="700" fill="#111">'
         f'Category presence by format, repositories with a single context file (% of files)</text>',
         f'<line x1="{L}" y1="{T - 44}" x2="{W - 24}" y2="{T - 44}" stroke="#111" stroke-width="1.2"/>',
         f'<text x="{L + 6}" y="{T - 17}" font-size="12" font-weight="700" fill="#111">Category</text>']
    for j, f in enumerate(formats):
        x = L + cw0 + j * cw + cw / 2
        o.append(f'<text x="{x}" y="{T - 24}" font-size="12" font-weight="700" text-anchor="middle" fill="#111">{labels[f]}</text>'
                 f'<text x="{x}" y="{T - 9}" font-size="11" text-anchor="middle" fill="#555">n = {n_per_format[f]}</text>')
    xv = L + cw0 + ncol * cw + vw / 2
    o.append(f'<text x="{xv}" y="{T - 17}" font-size="12" font-weight="700" text-anchor="middle" fill="#111">V</text>')
    o.append(f'<line x1="{L}" y1="{T}" x2="{W - 24}" y2="{T}" stroke="#111" stroke-width="0.7"/>')
    for i, r in enumerate(summary.itertuples()):
        y = T + i * rh
        if i % 2:
            o.append(f'<rect x="{L}" y="{y}" width="{cw0}" height="{rh}" fill="{STRIPE}"/>'
                     f'<rect x="{L + cw0 + ncol * cw}" y="{y}" width="{vw}" height="{rh}" fill="{STRIPE}"/>')
        name = esc(r.category) + (" †" if r.p >= alpha else "")
        o.append(f'<text x="{L + 6}" y="{y + rh / 2 + 4}" font-size="11.5" font-family="{MONO}" fill="#111">{name}</text>')
        vals = [summary.loc[r.Index, f"pct_{f}"] for f in formats]
        highest = max(round(v, 1) for v in vals)
        for j, v in enumerate(vals):
            x = L + cw0 + j * cw
            bold = ' font-weight="700"' if round(v, 1) == highest else ""
            o.append(f'<rect x="{x + 1}" y="{y + 1}" width="{cw - 2}" height="{rh - 2}" fill="{color(v, 85)}"/>'
                     f'<text x="{x + cw / 2}" y="{y + rh / 2 + 4}" font-size="12" text-anchor="middle" '
                     f'fill="{"#fff" if v > 62 else "#111"}"{bold}>{v:.1f}</text>')
        o.append(f'<text x="{xv}" y="{y + rh / 2 + 4}" font-size="12" text-anchor="middle" fill="#111">{r.cramer_v:.2f}</text>')
    yb = T + rh * len(summary)
    o.append(f'<line x1="{L}" y1="{yb}" x2="{W - 24}" y2="{yb}" stroke="#111" stroke-width="1.2"/>')
    o.append(f'<text x="{L}" y="{yb + 20}" font-size="11" fill="#555">Bold = highest share in the row. '
             f'V = Cramér\'s V (chi-square test of independence, df = {ncol - 1}).</text>')
    o.append(f'<text x="{L}" y="{yb + 38}" font-size="11" fill="#555">† Not significant (p ≥ 0.05); all others p &lt; 0.05. '
             f'{omitted} omitted.</text>')
    o.append("</svg>")
    return "".join(o)
