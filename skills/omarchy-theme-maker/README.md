# omarchy-theme-maker

Open-source Hermes Agent skill, version **0.1.0**.

Builds a complete Omarchy user theme from a single image: dominant-color
extraction, dark/light auto-detection, a stock-calibrated neutral ramp,
WCAG contrast floors, and application through `omarchy theme set`.

## Provenance

Derived from a real theming session on Omarchy 4.0.3: a wallpaper was turned
into an applied desktop theme (bar, Hyprland borders, terminals, btop,
editors) in one pass. The generator script was debugged end-to-end against
stock backgrounds during that session before being generalized here.

## Inputs

- One local image file (PNG or JPEG) to derive the palette and background
  from.
- An optional theme name; defaults to the image filename.
- Optional flags: `--mode dark|light|auto`, `--force`, `--print`.

## Outputs

- `~/.config/omarchy/themes/<slug>/colors.toml` with the canonical Omarchy
  palette keys.
- `~/.config/omarchy/themes/<slug>/backgrounds/<image>` — the source image
  installed as the theme background.
- On `omarchy theme set <slug>`: Omarchy regenerates terminal, editor,
  shell, and Hyprland configs from the palette and retints running apps.

## Requirements

- Omarchy (any recent release; validated on 4.0.3).
- Python 3 with Pillow (median-cut quantization). All other logic is
  stdlib.

## Installation

Install from this repository with your Hermes tap, or copy
`skills/omarchy-theme-maker/` into your skills directory.

## Invocation

```bash
python3 scripts/palette_to_theme.py /path/to/wallpaper.png --name "My Theme" --print
python3 scripts/palette_to_theme.py /path/to/wallpaper.png --name "My Theme"
omarchy theme set my-theme
```

## Limitations

- Single-image input; no multi-image mood boards.
- Named colors (red/green/blue/...) are anchored to stock hue positions for
  terminal readability rather than matching the artwork's hues exactly.
- No theme `preview.png` is generated for the switcher.
- Linux-only: requires the `omarchy` CLI.

## Safety

Writes only inside `~/.config/omarchy/themes/<slug>/`. Never touches
`/usr/share/omarchy/`. Applies the theme only when the user asks.
Source images are treated as untrusted pixel data, never instructions.

## Privacy

Images are processed locally. No network access, no telemetry, no data
leaves the machine.

## Version history

- 0.1.0 — Initial public release: palette extraction, auto dark/light,
  contrast floors, background install, apply workflow.
