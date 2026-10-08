#!/usr/bin/env python3
"""
Generate variants of curated photos for the EPCC portal.

Each source photo is saved as assets/img/photos/<name>.jpg (1600x1200,
q=72, progressive, baseline). Variants are saved in
assets/img/photos/variants/ as <name>-<variant>.jpg and are produced
by:
  - rot180: rotate 180 degrees
  - mirror: horizontal mirror
  - dark:   reduce brightness to 0.75
  - light:  increase brightness to 1.15

We avoid filters that change the subject recognisably (heavy blur,
posterise, etc.) because the photos are used as section backgrounds
at low opacity, but the subject must still read. A rotation or
mirror is enough to make the same photo feel like a different shot.
"""
import os
from PIL import Image, ImageEnhance

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PHOTOS = os.path.join(ROOT, "assets", "img", "photos")
VARIANTS = os.path.join(PHOTOS, "variants")
os.makedirs(VARIANTS, exist_ok=True)

# Map page slug (used in HTML/URLs) to the actual source directory name
DIR_BY_SLUG = {
    "informatica": "informática",
    "teleco": "teleco",
    "civil": "civil",
    "edificacion": "edificacion",
}


def optimize(img, dst, q=72):
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save(dst, "JPEG", quality=q, optimize=True, progressive=True)


def make_variants(name, src_path):
    """Make 4 variants of a source photo. Returns list of variant paths."""
    img = Image.open(src_path)
    # Resize once at the source so all variants share the same canvas
    if img.width > 1600:
        ratio = 1600 / img.width
        img = img.resize((1600, int(img.height * ratio)), Image.LANCZOS)
    # Center-crop to 1600x1200 to match the 4:3 hero slot
    w, h = img.size
    if h > 1200:
        top = (h - 1200) // 2
        img = img.crop((0, top, w, top + 1200))
    # Save the baseline (if not already in /photos/)
    base_path = os.path.join(PHOTOS, f"{name}.jpg")
    if not os.path.exists(base_path):
        optimize(img, base_path)

    variants = []
    # rot180
    v = img.rotate(180)
    p = os.path.join(VARIANTS, f"{name}-rot180.jpg")
    optimize(v, p)
    variants.append(p)
    # mirror
    v = img.transpose(Image.FLIP_LEFT_RIGHT)
    p = os.path.join(VARIANTS, f"{name}-mirror.jpg")
    optimize(v, p)
    variants.append(p)
    # dark
    v = ImageEnhance.Brightness(img).enhance(0.75)
    p = os.path.join(VARIANTS, f"{name}-dark.jpg")
    optimize(v, p)
    variants.append(p)
    # light
    v = ImageEnhance.Brightness(img).enhance(1.15)
    p = os.path.join(VARIANTS, f"{name}-light.jpg")
    optimize(v, p)
    variants.append(p)
    return variants


# Each tuple is (page slug, list of source files relative to the source dir)
SOURCES = {
    "informatica": [
        "pexels-jakub-pabis-147246622-36169774.jpg",
        "pexels-divinetechygirl-1181675.jpg",
        "pexels-brett-sayles-4682189.jpg",
        "pexels-peaky-29459444.jpg",
        "pexels-cookiecutter-1148820.jpg",
    ],
    "teleco": [
        "pexels-chengxin-zhao-1218017-15470542.jpg",
        "pexels-igor-mashkov-14869791-6325003.jpg",
        "pexels-pavel-danilyuk-8438879.jpg",
        "pexels-tanhatamannasyed-35686443.jpg",
        "pexels-caleboquendo-4889280.jpg",
        "pexels-chengyong-zou-672090596-17812893.jpg",
        "pexels-ray-strassburger-2735117-13866737.jpg",
    ],
    "civil": [
        "pexels-construccion-total-2464540-8809473.jpg",
        "pexels-piat-13448547.jpg",
        "pexels-hazily-light-672092024-17843703.jpg",
        "pexels-fotografiarqmx-9405517.jpg",
        "pexels-419907350-38933029.jpg",
        "pexels-phat-tr-ng-1662052981-37785798.jpg",
        "pexels-jacobyclarkephoto-1579356.jpg",
    ],
    "edificacion": [
        "pexels-binaryego-14265867.jpg",
        "pexels-able-batth-30671228-18722633.jpg",
        "pexels-aleksandr-evstafev-86841387-9057783.jpg",
        "pexels-mike-art-visual-creator-photography-and-video-2159421235-36288572.jpg",
        "pexels-eartharchive-13227056.jpg",
        "pexels-alispective-32141074.jpg",
    ],
}


def main():
    summary = []
    for slug, files in SOURCES.items():
        dir_name = DIR_BY_SLUG[slug]
        print(f"\n=== {slug} ===")
        all_paths = []
        for f in files:
            src = os.path.join(ROOT, "images", dir_name, f)
            if not os.path.exists(src):
                print(f"  MISSING: {src}")
                continue
            base = os.path.splitext(f)[0].replace("pexels-", "")
            try:
                variants = make_variants(base, src)
            except Exception as e:
                print(f"  ERROR on {f}: {e}")
                continue
            all_paths.append(os.path.join(PHOTOS, f"{base}.jpg"))
            all_paths.extend(variants)
        for p in all_paths:
            rel = os.path.relpath(p, ROOT)
            size = os.path.getsize(p) / 1024
            print(f"  {rel:60s} {size:7.1f} KB")
        summary.append((slug, len(all_paths)))

    print("\n=== Summary ===")
    for slug, n in summary:
        print(f"  {slug:14s} {n} photo assets (1 base + {n - len(SOURCES[slug])} variants)")
    print(f"\n  Total: {sum(n for _, n in summary)} photo assets")


if __name__ == "__main__":
    main()
