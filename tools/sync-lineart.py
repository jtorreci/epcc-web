#!/usr/bin/env python3
"""Copy the line-art sprite (assets/img/lineart.svg) into every page.

The drawings are inlined in each HTML page so they also render when a page
is opened from disk (file://). Edit only assets/img/lineart.svg, then run:

    python3 tools/sync-lineart.py

What it does:
  * adds pathLength="1" and vector-effect="non-scaling-stroke" to every
    drawable element that lacks them (needed for the draw-in effect);
  * warns about fill/stroke/style attributes (colours come from site.css);
  * replaces the <svg class="sprite"> block in each page;
  * checks that every drawing a page references exists in the sprite.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPRITE = ROOT / "assets/img/lineart.svg"
PAGES = ["index.html", "informatica.html", "teleco.html", "civil.html", "edificacion.html"]
SHAPES = ("path", "line", "polyline", "polygon", "rect", "circle", "ellipse")
SPRITE_BLOCK = re.compile(r'(<svg class="sprite"[^>]*>\n).*?(\n\s*</svg>)', re.S)


def normalize_shapes(svg: str) -> tuple[str, int]:
    """Add the attributes the draw-in effect needs to every shape element."""
    added = 0

    def fix(match: re.Match) -> str:
        nonlocal added
        tag = match.group(0)
        extra = ""
        if "pathLength=" not in tag:
            extra += ' pathLength="1"'
        if "vector-effect=" not in tag:
            extra += ' vector-effect="non-scaling-stroke"'
        if extra:
            added += 1
            end = "/>" if tag.endswith("/>") else ">"
            tag = tag[: -len(end)].rstrip() + extra + end
        return tag

    pattern = re.compile(r"<(?:%s)\b[^>]*?/?>" % "|".join(SHAPES), re.S)
    return pattern.sub(fix, svg), added


def main() -> int:
    source = SPRITE.read_text(encoding="utf-8")
    source, added = normalize_shapes(source)
    if added:
        SPRITE.write_text(source, encoding="utf-8")
        print(f"lineart.svg: added draw-in attributes to {added} element(s)")

    symbols = re.findall(r'<symbol[^>]*\bid="([^"]+)"', source)
    if not symbols:
        print("error: no <symbol id=...> found in lineart.svg", file=sys.stderr)
        return 1
    for sym in re.finditer(r'<symbol[^>]*\bid="([^"]+)"[^>]*>', source):
        if "viewBox=" not in sym.group(0):
            print(f"warning: symbol '{sym.group(1)}' has no viewBox (expected 0 0 800 600)")
    for attr in ("fill=", "stroke=", "style="):
        if re.search(r"<(?:%s)\b[^>]*\b%s" % ("|".join(SHAPES), attr), source):
            print(f"warning: shapes use '{attr[:-1]}'; colours and widths come from site.css")

    inner = source[source.index("<symbol") : source.rindex("</svg>")].strip()
    status = 0
    for name in PAGES:
        page = ROOT / name
        html = page.read_text(encoding="utf-8")
        if not SPRITE_BLOCK.search(html):
            print(f"error: {name} has no <svg class=\"sprite\"> block", file=sys.stderr)
            status = 1
            continue
        comment = "    <!-- Inlined line-art sprite (source: assets/img/lineart.svg) so drawings also render from file:// -->\n"
        html = SPRITE_BLOCK.sub(lambda m: m.group(1) + comment + "    " + inner + m.group(2), html, count=1)
        page.write_text(html, encoding="utf-8")

        used = re.findall(r'<use href="#([^"]+)"', html)
        missing = sorted(set(used) - set(symbols))
        if missing:
            print(f"error: {name} uses missing drawing(s): {', '.join(missing)}", file=sys.stderr)
            status = 1
        else:
            print(f"{name}: synced ({len(symbols)} drawings, {len(used)} used)")
    return status


if __name__ == "__main__":
    sys.exit(main())
