# PhotoStar app icon

A **camera with a star on its prism**: an engraving-style drawing, seen from the front, filling the
tile (full-bleed field, body and lens filling the frame, neck straps running off the edges). The
line work is hatching, knurling and stipple; the star on the prism is the "Star" in PhotoStar.

## Palette

Exactly three colours:

| Colour | Hex | Used for |
|---|---|---|
| Ink | `#0b0b0c` | line work and contours |
| Paper | `#efe9dc` | the figure |
| PhotoStar blue (app colour) | `#2f7bf5` | the full-bleed field |

## Geometry

A 512-unit tile (`viewBox="0 0 512 512"`), rounded square with `rx=112`, no border. The macOS
renders pad it onto Apple's 824/1024 icon grid; the Windows and Linux renders crop 22 units off
each side so the figure reads at 16–48 px.

## Provenance

Original artwork drawn as code by an AI assistant (Claude) for the PhotoStar fork, in the style of
the icon it replaces. `make_icon.py` in this directory writes `photostar.svg`; nothing is traced
from, or copied out of, another work. This replaces PhotoCraft's earlier fox icon. License: see
`LICENSE.txt`.

## Files

- `photostar.svg`: canonical master, written by `make_icon.py`.
- `photostar-small.svg`: same drawing; also the hicolor scalable icon.
- `photostar-1024.png`: 1024 px render on the macOS grid.
- `photostar.icns`: macOS bundle icon (`CFBundleIconFile`).
- `photostar.ico`: Windows icon, 16–256 px, embedded in the `.exe` by `apps/photostar/build.rs`.
- `hicolor/<size>/apps/ai.storyteller.photostar.png` (16–512) and `hicolor/scalable/...svg`:
  Linux icon theme.

The app also sets the window icon and Wayland app ID at runtime (`apps/photostar/src/app_icon.rs`,
`main.rs`). On Windows the taskbar shows the icon of the Start Menu shortcut that launches the
exe, so the MSI's `<Icon Id>` keeps the `.exe` extension (ICE50); `app_icon.rs` documents the
details and tests the `.ico` sizes and the WiX icon references.

## Regenerate

Edit `make_icon.py` and run `python3 assets/app-icon/make_icon.py assets/app-icon/photostar.svg`
(copy the result to `photostar-small.svg`), then run `packaging/icons.sh`. It needs `resvg`, plus
`iconutil` on macOS; the `.ico` is packed by `cargo xtask ico`.
