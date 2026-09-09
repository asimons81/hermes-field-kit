# Example: theming Omarchy from a wallpaper (successful run)

Session on Omarchy 4.0.3. The user supplied a dark cyberpunk wallpaper
(neon magenta field, cyan accents, black cityscape) and asked for a theme
named HermTang.

Steps:

1. Inspected the image (brightness, dominant colors, accent candidates).
2. Dry-run:
   `python3 scripts/palette_to_theme.py wallpaper.png --name "HermTang" --print`
   Output head: `mode = "dark"`, `accent = "#c403a9"`, near-black
   pink-tinted background ramp, foreground at 9.25:1 contrast.
3. Real run created `~/.config/omarchy/themes/hermtang/colors.toml` and
   `backgrounds/wallpaper.png`.
4. `omarchy theme set hermtang`.
5. Verification: `omarchy theme current` printed `Hermtang`; the shell
   accent and Hyprland active border rendered as `#c403a9`; the background
   symlink pointed at the staged image.

Takeaway: auto mode landed dark (weighted luminance 0.30) and the magenta
accent passed contrast (3.63:1) without manual adjustment.

# Example: boundary — mixed-brightness image defeats auto mode

A mostly-white artwork with dark subject silhouettes produced a weighted
luminance near the 0.5 threshold; auto mode picked dark and the resulting
near-black ramp fought the wallpaper's white field.

Resolution: rerun with `--mode light`, which emitted the light ramp
(`background = "#f2f4f5"`, orange accent) that matched the artwork. The
correct move for ambiguous images is an explicit mode, decided by asking
the user or judging the image's dominant field, not the threshold.
