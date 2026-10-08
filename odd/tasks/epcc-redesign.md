# Feature: epcc-redesign

## Objective
Modernize the EPCC promotional site (reached via printed QR) into a flat, low-interactivity static site with a three-layer parallax (background / line-art middle layer / foreground content) and one dedicated page per degree (+ its master).

## Problem / Why
- Current site is a single generic landing page (emoji icons, gradients, modals).
- Degrees only exist as JS modals: not linkable, not QR-addressable.
- Informática and Telecomunicación data is outdated.

## Scope
- Shared stylesheet + shared line-art SVG layer, plain HTML, no build step, no framework.
- Pages: `index.html` (portal), `informatica.html`, `teleco.html`, `civil.html`, `edificacion.html`.
- Updated degree data:
  - Informática: ONE degree, four menciones from 3rd year: Ingeniería de Software, Ingeniería de Computadores, Ciberseguridad, Ciencia de Datos.
  - Telecomunicación: degree with two menciones: Sistemas de Telecomunicación, Imagen y Sonido (previously Sonido e Imagen only).
- Masters integrated in each degree page.

## Constraints
- Static files only, deployable by existing GitHub Pages workflow (path '.').
- `index.html` stays as entry point (QR target).
- Minimal JS; parallax must degrade gracefully (prefers-reduced-motion, no scroll-timeline support).
- Spanish UI copy with full accents.

## Delivery strategy
ask-on-risk. Forecast: ~1500+ authored lines (generated static pages) — chain strategy to be asked before PR.

## Tasks
- [x] T1 Collect verified official data (epcc.unex.es) — route: delegated research (mapping trigger: external evidence)
  - Informática: Grado en Ingeniería Informática (plan 1647, RD 822/2021, from 2026/27), 240 ECTS, 160 plazas; Cáceres menciones from 3rd year: Ingeniería del Software, Ingeniería de Computadores, Ciencia de Datos, Ciberseguridad. https://epcc.unex.es/titulaciones/1647
  - Teleco: Grado en Ingeniería de Tecnologías de Telecomunicación (plan 1648, from 2026/27), 240 ECTS, 60 plazas; Cáceres menciones: Sistemas de Telecomunicación, Sonido e Imagen (official order/name). https://epcc.unex.es/titulaciones/1648
  - Civil (1640): 240 ECTS, ITOP; menciones Construcciones Civiles, Hidrología, Transportes y Servicios Urbanos (two possible).
  - Edificación (1626): 240 ECTS, Arquitecto Técnico, 40 plazas, no menciones.
  - Double degrees ADE + Informática (feet.unex.es 1492/1493) still offered, 6 years, 13 plazas each.
  - Masters: MU Ing. Informática (1650, 90 ECTS), MU Ing. Telecomunicación (1649, 90 ECTS, habilitante), MU Ing. Caminos, Canales y Puertos (1641, 120 ECTS, habilitante), MU BIM (1645, 60 ECTS, semipresencial), MU Investigación en Ingeniería y Arquitectura (1646, 60 ECTS).
  - EUR-ACE seal NOT verified for any degree -> removed from copy.
  - Contact: Avda. Universidad s/n, 10003 Cáceres; 927 257 195; secretaria_epcc@unex.es
- [ ] T2 Design system + shared assets (`assets/css/site.css`, line-art SVGs, parallax) — route: delegated writer (2+ non-trivial files)
- [ ] T3 Portal `index.html` rewrite — route: delegated writer
- [ ] T4 Degree pages (4) with masters — route: delegated writer
- [ ] T5 Structural verification (links, accents, reduced-motion, mobile width) — route: delegated verifier

## Acceptance criteria
- Each degree reachable at its own URL; portal links to all.
- No outdated Informática/Teleco data remains.
- Works without JS; parallax layers visible on scroll in modern browsers; static fallback otherwise.

## Progress / Evidence
- Normalized CRLF-only diff on index.html (`git checkout -- index.html`); branch `feat/redesign-parallax-degree-pages`.

## Next step
T1 research in progress.
