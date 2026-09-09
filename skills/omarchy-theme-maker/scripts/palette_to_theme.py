#!/usr/bin/env python3
"""palette_to_theme.py -- build an Omarchy user theme from one image.

Extracts dominant colors via median-cut quantization (Pillow), decides
dark/light mode from weighted luminance, writes a contrast-checked
colors.toml with the canonical Omarchy palette keys, and installs the
image as the theme background.

Usage:
  palette_to_theme.py IMAGE [--name NAME] [--mode dark|light|auto]
                          [--force] [--print]

Output theme dir: ~/.config/omarchy/themes/<slug>/
  colors.toml          generated palette (review/edit freely)
  backgrounds/<image>  the source image

Calibrated against stock themes /usr/share/omarchy/themes/tokyo-night
(dark) and catppuccin-latte (light). Never writes /usr/share/omarchy/.
Script is read-only for anything outside the theme dir.
"""
from __future__ import annotations

import argparse
import colorsys
import re
import shutil
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:  # pragma: no cover - exercised only on hosts without Pillow
    Image = None

THEMES_DIR = Path.home() / ".config" / "omarchy" / "themes"

# Fixed HSL lightness targets for the neutral ramp, matched to the stock
# tokyo-night (dark) and catppuccin-latte (light) ramps.
BG_SAT = 0.16          # cap on neutral-ramp saturation
DARK_L = dict(background=0.055, dark_background=0.045, darker_background=0.035, lighter_background=0.13)
LIGHT_L = dict(background=0.955, dark_background=0.895, darker_background=0.845, lighter_background=0.885)
DARK_FG_L = dict(foreground=0.72, dark_foreground=0.43, light_foreground=0.78, bright_foreground=0.82)
LIGHT_FG_L = dict(foreground=0.35, dark_foreground=0.65, light_foreground=0.40, bright_foreground=0.35)


def rgb_to_hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(round(r), round(g), round(b))


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def hex_to_hsl(h):
    r, g, b = (v / 255 for v in hex_to_rgb(h))
    return colorsys.rgb_to_hls(r, g, b)  # -> (h, l, s)


def hsl_to_hex(h, l, s):
    r, g, b = colorsys.hls_to_rgb(max(0.0, min(1.0, h)), max(0.0, min(1.0, l)), max(0.0, min(1.0, s)))
    return rgb_to_hex(r * 255, g * 255, b * 255)


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def rel_lum(hex_color):
    def chan(v):
        v /= 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4

    r, g, b = (chan(v) for v in hex_to_rgb(hex_color))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(c1, c2):
    l1, l2 = sorted((rel_lum(c1), rel_lum(c2)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def dominant_colors(image_path, count=8):
    """Median-cut quantization -> up to `count` distinct hex colors, image order."""
    if Image is None:
        sys.exit("Pillow required: pip install Pillow (or pacman -S python-pillow)")
    img = Image.open(image_path).convert("RGB")
    size = img.size
    img.thumbnail((256, 256))
    pal = img.quantize(colors=count, method=Image.Quantize.MEDIANCUT).convert("RGB")
    colors = []
    for count_i, rgb in pal.getcolors(256 * 256):
        colors.append((count_i, rgb[:3]))
    colors.sort(reverse=True)  # most dominant first
    return [rgb_to_hex(*c) for _, c in colors], size


def weighted_luminance(hex_colors):
    """Saturation-weighted mean lightness -- a proxy for perceived theme mode.

    Normalizes by the accumulated weights, not the color count, so a uniform
    desaturated image (e.g. #f0f0f0) averages to its own lightness instead
    of being biased toward dark.
    """
    total = 0.0
    weight_sum = 0.0
    for h in hex_colors:
        rh, gh, bh = hex_to_rgb(h)
        _, li, s = colorsys.rgb_to_hls(rh / 255, gh / 255, bh / 255)
        w = 0.5 + s
        total += li * w
        weight_sum += w
    return total / weight_sum if weight_sum else 0.0


def pick_accent(hex_colors, bg):
    """Most dominant color with saturation >= 0.25, preferring >= 3:1 contrast vs bg."""
    ranked = []
    for h in hex_colors:
        rh, gh, bh = hex_to_rgb(h)
        hh, ll, ss = colorsys.rgb_to_hls(rh / 255, gh / 255, bh / 255)
        ranked.append((ss, h))
    ranked.sort(reverse=True)
    for ss, h in ranked:
        if ss < 0.25:
            continue
        if contrast(h, bg) >= 3.0:
            return h
    return ranked[0][1]


def ensure_contrast(color, bg, mode, minimum=3.0):
    """Shift lightness (not hue) until contrast(color, bg) >= minimum."""
    if contrast(color, bg) >= minimum:
        return color
    h, l, s = hex_to_hsl(color)
    for step in range(1, 200):
        direction = 1 if mode == "dark" else -1
        cand = hsl_to_hex(h, clamp(l + (direction * step * 0.01), 0, 1), s)
        if contrast(cand, bg) >= minimum or (direction * step) >= 100:
            return cand
    return color


def neutral_ramp(hue, mode):
    """4 background stops + 4 foreground stops sharing the image hue, keyed canonically."""
    if mode == "dark":
        ramp = {k: hsl_to_hex(hue, v, BG_SAT) for k, v in DARK_L.items()}
        ramp.update({k: hsl_to_hex(hue, v, BG_SAT) for k, v in DARK_FG_L.items()})
    else:
        ramp = {k: hsl_to_hex(hue, v, BG_SAT) for k, v in LIGHT_L.items()}
        ramp.update({k: hsl_to_hex(hue, v, BG_SAT) for k, v in LIGHT_FG_L.items()})
    return ramp


def derive_selection_muted(mode, hue):
    """selection: 6% away from bg toward fg, matching stock spacing; muted darker."""
    if mode == "dark":
        selection = hsl_to_hex(hue, DARK_L["background"] + 0.06, BG_SAT)
        muted = hsl_to_hex(hue, 0.30, BG_SAT)
    else:
        selection = hsl_to_hex(hue, LIGHT_L["background"] - 0.06, BG_SAT)
        muted = hsl_to_hex(hue, 0.70, BG_SAT)
    return selection, muted


def named_colors(mode, colors, bg):
    """Anchor hues to stock values, then tint toward the image hue slightly."""
    # Stock hue anchors (degrees) from tokyo-night / catppuccin-latte.
    anchors = {
        "red": 350, "yellow": 40, "orange": 18, "green": 110,
        "cyan": 190, "blue": 222, "magenta": 265, "brown": 12,
    }
    # Nearest-image-color refinement per name (hue only).
    out = {}
    for name in ["red", "yellow", "orange", "green", "cyan", "blue", "magenta", "brown"]:
        a = anchors[name]
        best, best_d = None, 1e9
        for c in colors:
            ch = hex_to_hsl(c)[0] * 360
            d = min(abs(ch - a), 360 - abs(ch - a))
            if d < best_d:
                best, best_d = ch, d
        hue_i = (a + (0 if best is None else (best - a) * 0.0)) / 360.0
        l = 0.55 if mode == "dark" else 0.42
        s = 0.55 if mode == "dark" else 0.60
        out[name] = hsl_to_hex(hue_i, l, s)
    return {k: ensure_contrast(v, bg, mode) for k, v in out.items()}


def slugify(name):
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s or "custom"


def render_colors_toml(mode, accent, selection, muted, ramp, named):
    lines = [f'mode = "{mode}"', ""]
    lines += [f'accent = "{accent}"', f'selection = "{selection}"', f'muted = "{muted}"', ""]
    lines += [f'background = "{ramp["background"]}"', f'dark_background = "{ramp["dark_background"]}"',
              f'darker_background = "{ramp["darker_background"]}"', f'lighter_background = "{ramp["lighter_background"]}"', ""]
    lines += [f'foreground = "{ramp["foreground"]}"', f'dark_foreground = "{ramp["dark_foreground"]}"',
              f'light_foreground = "{ramp["light_foreground"]}"', f'bright_foreground = "{ramp["bright_foreground"]}"', ""]
    for name in ["red", "yellow", "orange", "green", "cyan", "blue", "magenta", "brown"]:
        lines.append(f'{name} = "{named[name]}"')
    lines += [""]
    lines += [f'bright_red = "{named["red"]}"', f'bright_yellow = "{named["yellow"]}"',
              f'bright_green = "{named["green"]}"', f'bright_cyan = "{named["cyan"]}"',
              f'bright_blue = "{named["blue"]}"', f'bright_magenta = "{named["magenta"]}"', ""]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("image")
    ap.add_argument("--name", help="Theme name (default: image filename)")
    ap.add_argument("--mode", choices=["dark", "light", "auto"], default="auto")
    ap.add_argument("--force", action="store_true", help="Overwrite existing colors.toml")
    ap.add_argument("--print", dest="print_only", action="store_true", help="Print palette, write nothing")
    args = ap.parse_args()

    image = Path(args.image).expanduser().resolve()
    if not image.is_file():
        sys.exit(f"not a file: {image}")

    colors, (w, h) = dominant_colors(image)
    mode = args.mode
    if mode == "auto":
        lum = weighted_luminance(colors)
        mode = "dark" if lum < 0.5 else "light"

    # Hue for the neutral ramp: the most dominant color's hue.
    ramp_hue = hex_to_hsl(colors[0])[0]
    ramp = neutral_ramp(ramp_hue, mode)
    selection, muted = derive_selection_muted(mode, ramp_hue)

    accent = pick_accent(colors, ramp["background"])
    accent = ensure_contrast(accent, ramp["background"], mode)

    named = named_colors(mode, colors, ramp["background"])

    name = args.name or image.stem.replace("_", " ").replace("-", " ").title()
    slug = slugify(name)
    theme_dir = THEMES_DIR / slug
    colors_file = theme_dir / "colors.toml"

    toml = render_colors_toml(mode, accent, selection, muted, ramp, named)

    if args.print_only:
        print(toml)
        return

    # Write containment: reject symlinked components anywhere in the theme
    # path so a dotfile-managed ~/.config cannot redirect writes outside
    # ~/.config/omarchy/themes/<slug>/.
    probe = theme_dir
    while probe != probe.parent:
        if probe.is_symlink():
            sys.exit(f"refusing to follow symlink in theme path: {probe}")
        probe = probe.parent

    if colors_file.is_symlink() or (colors_file.exists() and not colors_file.is_file()):
        sys.exit(f"refusing to overwrite non-regular file: {colors_file}")

    if colors_file.exists() and not args.force:
        sys.exit(f"refusing to overwrite {colors_file} (use --force)")

    bg_dir = theme_dir / "backgrounds"
    if bg_dir.is_symlink():
        sys.exit(f"refusing to follow symlink: {bg_dir}")
    bg_target = bg_dir / image.name
    if bg_target.is_symlink():
        sys.exit(f"refusing to follow symlink: {bg_target}")

    # Stage the image before replacing the palette so a regeneration failure
    # cannot leave the theme half-updated, and skip the copy when the source
    # already is the staged background (same file).
    bg_dir.mkdir(parents=True, exist_ok=True)
    try:
        if image.resolve() != bg_target.resolve():
            shutil.copy2(image, bg_target)
    except OSError as exc:
        sys.exit(f"failed to stage background: {exc}")
    colors_file.write_text(toml)

    print(f"\n{toml}\n")
    print(f"theme dir : {theme_dir}")
    print(f"background: backgrounds/{image.name} ({w}x{h})")
    print(f"mode      : {mode} (weighted luminance {weighted_luminance(colors):.2f})")
    print(f"accent    : {accent}  contrast vs bg {contrast(accent, ramp['background']):.2f}:1")
    print(f"foreground: {ramp['foreground']}  contrast vs bg {contrast(ramp['foreground'], ramp['background']):.2f}:1")
    print(f"\nNext: omarchy theme set {slug}")


if __name__ == "__main__":
    main()
