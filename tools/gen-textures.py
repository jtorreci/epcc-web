#!/usr/bin/env python3
"""
Generate dark, abstract SVG background textures for the EPCC portal.

Each texture is a 1600x1000 SVG with:
- A radial gradient base in charcoal tones (matches the site dark theme).
- A subtle line pattern in the same technical-drawing language as the
  parallax sprite (straight lines, soft curves, very low opacity).
- A gold-accent glow positioned off-centre.

The output is small (~3-6 KB) and renders crisply at any size.
"""
import os
import random

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "img")
os.makedirs(OUT_DIR, exist_ok=True)


def wrap(name, viewbox, body, defs):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" preserveAspectRatio="xMidYMid slice" role="img" aria-label="{name}">
  <defs>
{defs}
  </defs>
{body}
</svg>
'''


def base_layer():
    return '  <rect width="100%" height="100%" fill="url(#bg)"/>\n'


def accent_glow(cx, cy, r, opacity=0.18):
    return f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#glow)" opacity="{opacity}"/>\n'


# Pattern definitions
PATTERNS = {
    "hero": {
        # Abstract constellation: scattered nodes + connecting lines
        "defs": '''    <radialGradient id="bg" cx="30%" cy="40%" r="80%">
      <stop offset="0%" stop-color="#2a2d33"/>
      <stop offset="100%" stop-color="#15161a"/>
    </radialGradient>
    <radialGradient id="glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#f0b90b"/>
      <stop offset="100%" stop-color="#f0b90b" stop-opacity="0"/>
    </radialGradient>''',
        "body": "".join([
            base_layer(),
            accent_glow(1200, 200, 500, 0.10),
            # Nodes
            '  <g fill="none" stroke="#ece8df" stroke-width="1" opacity="0.18">\n',
            '    <circle cx="200" cy="180" r="6"/>\n',
            '    <circle cx="450" cy="120" r="4"/>\n',
            '    <circle cx="780" cy="240" r="8"/>\n',
            '    <circle cx="1100" cy="160" r="5"/>\n',
            '    <circle cx="1350" cy="320" r="7"/>\n',
            '    <circle cx="320" cy="520" r="5"/>\n',
            '    <circle cx="640" cy="600" r="9"/>\n',
            '    <circle cx="960" cy="480" r="4"/>\n',
            '    <circle cx="1240" cy="640" r="6"/>\n',
            '    <circle cx="180" cy="780" r="5"/>\n',
            '    <circle cx="520" cy="820" r="7"/>\n',
            '    <circle cx="880" cy="760" r="4"/>\n',
            '    <circle cx="1180" cy="880" r="6"/>\n',
            '  </g>\n',
            # Connecting lines (constellation)
            '  <g fill="none" stroke="#ece8df" stroke-width="0.6" opacity="0.10">\n',
            '    <path d="M200 180L450 120L780 240L1100 160L1350 320"/>\n',
            '    <path d="M320 520L640 600L960 480L1240 640"/>\n',
            '    <path d="M180 780L520 820L880 760L1180 880"/>\n',
            '    <path d="M200 180L320 520L180 780"/>\n',
            '    <path d="M450 120L640 600L520 820"/>\n',
            '    <path d="M780 240L960 480L880 760"/>\n',
            '    <path d="M1100 160L1240 640L1180 880"/>\n',
            '    <path d="M1350 320L1240 640L1180 880"/>\n',
            '  </g>\n',
        ]),
    },
    "informatica": {
        # Circuit-style grid: horizontal/vertical lines + nodes
        "defs": '''    <radialGradient id="bg" cx="70%" cy="30%" r="90%">
      <stop offset="0%" stop-color="#252830"/>
      <stop offset="100%" stop-color="#14151a"/>
    </radialGradient>
    <radialGradient id="glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#f0b90b"/>
      <stop offset="100%" stop-color="#f0b90b" stop-opacity="0"/>
    </radialGradient>''',
        "body": "".join([
            base_layer(),
            accent_glow(1300, 800, 600, 0.08),
            # Vertical and horizontal lines, low opacity
            '  <g fill="none" stroke="#ece8df" stroke-width="0.8" opacity="0.10">\n',
            '    <path d="M0 200H1600M0 400H1600M0 600H1600M0 800H1600"/>\n',
            '    <path d="M200 0V1000M400 0V1000M600 0V1000M800 0V1000M1000 0V1000M1200 0V1000M1400 0V1000"/>\n',
            '  </g>\n',
            # Circuit traces
            '  <g fill="none" stroke="#ece8df" stroke-width="1.2" opacity="0.22">\n',
            '    <path d="M100 300H400V500H700V300H1000V500H1300"/>\n',
            '    <path d="M100 700H300V500H500V700H800V500H1100V700H1500"/>\n',
            '    <path d="M600 100V250H800V400M1000 100V250H1200V400"/>\n',
            '  </g>\n',
            # Nodes at line ends
            '  <g fill="#ece8df" opacity="0.35">\n',
            '    <circle cx="100" cy="300" r="4"/>\n',
            '    <circle cx="1300" cy="500" r="4"/>\n',
            '    <circle cx="100" cy="700" r="4"/>\n',
            '    <circle cx="1500" cy="700" r="4"/>\n',
            '    <circle cx="600" cy="100" r="3"/>\n',
            '    <circle cx="1000" cy="100" r="3"/>\n',
            '    <circle cx="800" cy="400" r="5"/>\n',
            '    <circle cx="1200" cy="400" r="3"/>\n',
            '  </g>\n',
        ]),
    },
    "teleco": {
        # Signal waves: concentric arcs radiating from a point
        "defs": '''    <radialGradient id="bg" cx="20%" cy="60%" r="80%">
      <stop offset="0%" stop-color="#22252c"/>
      <stop offset="100%" stop-color="#131419"/>
    </radialGradient>
    <radialGradient id="glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#f0b90b"/>
      <stop offset="100%" stop-color="#f0b90b" stop-opacity="0"/>
    </radialGradient>''',
        "body": "".join([
            base_layer(),
            accent_glow(200, 600, 700, 0.10),
            # Concentric arcs (signal)
            '  <g fill="none" stroke="#ece8df" stroke-width="1" opacity="0.18">\n',
            '    <circle cx="200" cy="600" r="100"/>\n',
            '    <circle cx="200" cy="600" r="200" opacity="0.7"/>\n',
            '    <circle cx="200" cy="600" r="300" opacity="0.5"/>\n',
            '    <circle cx="200" cy="600" r="400" opacity="0.4"/>\n',
            '    <circle cx="200" cy="600" r="500" opacity="0.3"/>\n',
            '    <circle cx="200" cy="600" r="600" opacity="0.2"/>\n',
            '  </g>\n',
            # Tower / antenna vertical line
            '  <g fill="none" stroke="#ece8df" stroke-width="1.5" opacity="0.30">\n',
            '    <path d="M200 600V200"/>\n',
            '    <path d="M180 250H220M170 320H230M160 400H240"/>\n',
            '    <circle cx="200" cy="200" r="6"/>\n',
            '  </g>\n',
            # Diagonal signal lines
            '  <g fill="none" stroke="#ece8df" stroke-width="0.8" opacity="0.12">\n',
            '    <path d="M400 400L800 300L1200 350L1500 280"/>\n',
            '    <path d="M400 500L800 480L1200 510L1500 470"/>\n',
            '    <path d="M400 800L800 820L1200 790L1500 810"/>\n',
            '  </g>\n',
        ]),
    },
    "civil": {
        # Structural lines: bridges, arches, perspective
        "defs": '''    <radialGradient id="bg" cx="50%" cy="20%" r="90%">
      <stop offset="0%" stop-color="#23262d"/>
      <stop offset="100%" stop-color="#14151a"/>
    </radialGradient>
    <radialGradient id="glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#f0b90b"/>
      <stop offset="100%" stop-color="#f0b90b" stop-opacity="0"/>
    </radialGradient>''',
        "body": "".join([
            base_layer(),
            accent_glow(800, 100, 500, 0.08),
            # Bridge arch
            '  <g fill="none" stroke="#ece8df" stroke-width="1.5" opacity="0.25">\n',
            '    <path d="M100 700Q800 400 1500 700"/>\n',
            '    <path d="M100 750Q800 450 1500 750" opacity="0.5"/>\n',
            '  </g>\n',
            # Vertical supports
            '  <g fill="none" stroke="#ece8df" stroke-width="1" opacity="0.18">\n',
            '    <path d="M300 700V900M500 600V900M700 510V900M900 510V900M1100 600V900M1300 700V900"/>\n',
            '  </g>\n',
            # Horizon line and ground
            '  <g fill="none" stroke="#ece8df" stroke-width="1" opacity="0.30">\n',
            '    <path d="M0 900H1600"/>\n',
            '  </g>\n',
            # Perspective lines (road)
            '  <g fill="none" stroke="#ece8df" stroke-width="0.6" opacity="0.12">\n',
            '    <path d="M0 900L800 500M1600 900L800 500M0 1000L800 500M1600 1000L800 500"/>\n',
            '  </g>\n',
            # Nodes
            '  <g fill="#ece8df" opacity="0.40">\n',
            '    <circle cx="300" cy="700" r="3"/>\n',
            '    <circle cx="500" cy="600" r="3"/>\n',
            '    <circle cx="700" cy="510" r="4"/>\n',
            '    <circle cx="900" cy="510" r="4"/>\n',
            '    <circle cx="1100" cy="600" r="3"/>\n',
            '    <circle cx="1300" cy="700" r="3"/>\n',
            '  </g>\n',
        ]),
    },
    "edificacion": {
        # Architectural grid: building outline + floor lines
        "defs": '''    <radialGradient id="bg" cx="80%" cy="40%" r="85%">
      <stop offset="0%" stop-color="#262930"/>
      <stop offset="100%" stop-color="#15161a"/>
    </radialGradient>
    <radialGradient id="glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#f0b90b"/>
      <stop offset="100%" stop-color="#f0b90b" stop-opacity="0"/>
    </radialGradient>''',
        "body": "".join([
            base_layer(),
            accent_glow(1400, 200, 600, 0.08),
            # Building outline
            '  <g fill="none" stroke="#ece8df" stroke-width="1.2" opacity="0.30">\n',
            '    <path d="M400 200H1200V900H400Z"/>\n',
            '    <path d="M500 200V900M700 200V900M900 200V900M1100 200V900"/>\n',
            '    <path d="M400 350H1200M400 500H1200M400 650H1200M400 800H1200"/>\n',
            '  </g>\n',
            # Window grid
            '  <g fill="#ece8df" opacity="0.15">\n',
            '    <rect x="450" y="280" width="30" height="40"/>\n',
            '    <rect x="520" y="280" width="30" height="40"/>\n',
            '    <rect x="600" y="280" width="30" height="40"/>\n',
            '    <rect x="730" y="280" width="30" height="40"/>\n',
            '    <rect x="800" y="280" width="30" height="40"/>\n',
            '    <rect x="930" y="280" width="30" height="40"/>\n',
            '    <rect x="1000" y="280" width="30" height="40"/>\n',
            '    <rect x="1110" y="280" width="30" height="40"/>\n',
            '    <rect x="450" y="430" width="30" height="40"/>\n',
            '    <rect x="600" y="430" width="30" height="40"/>\n',
            '    <rect x="730" y="430" width="30" height="40"/>\n',
            '    <rect x="870" y="430" width="30" height="40"/>\n',
            '    <rect x="1000" y="430" width="30" height="40"/>\n',
            '    <rect x="1110" y="430" width="30" height="40"/>\n',
            '    <rect x="520" y="580" width="30" height="40"/>\n',
            '    <rect x="660" y="580" width="30" height="40"/>\n',
            '    <rect x="800" y="580" width="30" height="40"/>\n',
            '    <rect x="930" y="580" width="30" height="40"/>\n',
            '    <rect x="1060" y="580" width="30" height="40"/>\n',
            '    <rect x="450" y="730" width="30" height="40"/>\n',
            '    <rect x="600" y="730" width="30" height="40"/>\n',
            '    <rect x="730" y="730" width="30" height="40"/>\n',
            '    <rect x="870" y="730" width="30" height="40"/>\n',
            '    <rect x="1000" y="730" width="30" height="40"/>\n',
            '    <rect x="1110" y="730" width="30" height="40"/>\n',
            '  </g>\n',
            # Ground line
            '  <g fill="none" stroke="#ece8df" stroke-width="1" opacity="0.25">\n',
            '    <path d="M0 900H1600"/>\n',
            '  </g>\n',
            # Door
            '  <g fill="none" stroke="#ece8df" stroke-width="1" opacity="0.40">\n',
            '    <path d="M750 900V820H850V900"/>\n',
            '  </g>\n',
        ]),
    },
    "empleo": {
        # Office grid: desks / workspaces as rectangles
        "defs": '''    <radialGradient id="bg" cx="40%" cy="50%" r="80%">
      <stop offset="0%" stop-color="#22252c"/>
      <stop offset="100%" stop-color="#13141a"/>
    </radialGradient>
    <radialGradient id="glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#f0b90b"/>
      <stop offset="100%" stop-color="#f0b90b" stop-opacity="0"/>
    </radialGradient>''',
        "body": "".join([
            base_layer(),
            accent_glow(600, 400, 600, 0.08),
            # Desk grid
            '  <g fill="none" stroke="#ece8df" stroke-width="1" opacity="0.22">\n',
            '    <rect x="100" y="200" width="200" height="100"/>\n',
            '    <rect x="400" y="200" width="200" height="100"/>\n',
            '    <rect x="700" y="200" width="200" height="100"/>\n',
            '    <rect x="1000" y="200" width="200" height="100"/>\n',
            '    <rect x="1300" y="200" width="200" height="100"/>\n',
            '    <rect x="100" y="500" width="200" height="100"/>\n',
            '    <rect x="400" y="500" width="200" height="100"/>\n',
            '    <rect x="700" y="500" width="200" height="100"/>\n',
            '    <rect x="1000" y="500" width="200" height="100"/>\n',
            '    <rect x="1300" y="500" width="200" height="100"/>\n',
            '    <rect x="100" y="800" width="200" height="100"/>\n',
            '    <rect x="400" y="800" width="200" height="100"/>\n',
            '    <rect x="700" y="800" width="200" height="100"/>\n',
            '    <rect x="1000" y="800" width="200" height="100"/>\n',
            '    <rect x="1300" y="800" width="200" height="100"/>\n',
            '  </g>\n',
            # People silhouettes (head circles)
            '  <g fill="#ece8df" opacity="0.20">\n',
            '    <circle cx="200" cy="250" r="14"/>\n',
            '    <circle cx="500" cy="250" r="14"/>\n',
            '    <circle cx="800" cy="250" r="14"/>\n',
            '    <circle cx="1100" cy="250" r="14"/>\n',
            '    <circle cx="1400" cy="250" r="14"/>\n',
            '    <circle cx="200" cy="550" r="14"/>\n',
            '    <circle cx="500" cy="550" r="14"/>\n',
            '    <circle cx="800" cy="550" r="14"/>\n',
            '    <circle cx="1100" cy="550" r="14"/>\n',
            '    <circle cx="1400" cy="550" r="14"/>\n',
            '    <circle cx="200" cy="850" r="14"/>\n',
            '    <circle cx="500" cy="850" r="14"/>\n',
            '    <circle cx="800" cy="850" r="14"/>\n',
            '    <circle cx="1100" cy="850" r="14"/>\n',
            '    <circle cx="1400" cy="850" r="14"/>\n',
            '  </g>\n',
        ]),
    },
    "movilidad": {
        # World grid: lat/long lines + route arcs
        "defs": '''    <radialGradient id="bg" cx="50%" cy="50%" r="90%">
      <stop offset="0%" stop-color="#22252c"/>
      <stop offset="100%" stop-color="#13141a"/>
    </radialGradient>
    <radialGradient id="glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#f0b90b"/>
      <stop offset="100%" stop-color="#f0b90b" stop-opacity="0"/>
    </radialGradient>''',
        "body": "".join([
            base_layer(),
            accent_glow(800, 500, 700, 0.08),
            # Longitude curves
            '  <g fill="none" stroke="#ece8df" stroke-width="0.8" opacity="0.10">\n',
            '    <path d="M200 100Q400 500 200 900"/>\n',
            '    <path d="M500 100Q700 500 500 900"/>\n',
            '    <path d="M800 100Q1000 500 800 900"/>\n',
            '    <path d="M1100 100Q1300 500 1100 900"/>\n',
            '    <path d="M1400 100Q1600 500 1400 900"/>\n',
            '  </g>\n',
            # Latitude lines
            '  <g fill="none" stroke="#ece8df" stroke-width="0.6" opacity="0.10">\n',
            '    <path d="M0 200Q800 250 1600 200"/>\n',
            '    <path d="M0 400Q800 450 1600 400"/>\n',
            '    <path d="M0 600Q800 650 1600 600"/>\n',
            '    <path d="M0 800Q800 850 1600 800"/>\n',
            '  </g>\n',
            # Route arcs (Caceres -> Europe)
            '  <g fill="none" stroke="#ece8df" stroke-width="1.2" opacity="0.30">\n',
            '    <path d="M700 600Q500 300 300 250"/>\n',
            '    <path d="M700 600Q800 350 900 280"/>\n',
            '    <path d="M700 600Q1100 350 1200 280"/>\n',
            '  </g>\n',
            # Origin marker (Caceres) and destination markers
            '  <g fill="#ece8df">\n',
            '    <circle cx="700" cy="600" r="6" opacity="0.6"/>\n',
            '    <circle cx="300" cy="250" r="4" opacity="0.5"/>\n',
            '    <circle cx="900" cy="280" r="4" opacity="0.5"/>\n',
            '    <circle cx="1200" cy="280" r="4" opacity="0.5"/>\n',
            '  </g>\n',
        ]),
    },
}


def main():
    for name, cfg in PATTERNS.items():
        svg = wrap(name, "0 0 1600 1000", cfg["body"], cfg["defs"])
        path = os.path.join(OUT_DIR, f"bg-{name}.svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        size = os.path.getsize(path)
        print(f"  {name:14s} -> {path} ({size} bytes)")


if __name__ == "__main__":
    main()
