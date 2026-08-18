# Exhibition Mode (`1fa82700`)

Dual-screen movie loop for kiosk **Exhibition Mode** (`nonInteractiveMode` in save data). Replaces the interactive game selector with synchronized TV + GamePad videos.

- **Title ID:** `000500001FA82700`
- **MLC path:** `mlc/usr/title/00050000/1fa82700/`
- **RPX:** `exhibition_wrapper.rpx` (install-only stub; Kiosk Menu does not launch it for playback)
- **User files:** `meta/TV00.mp4` … `meta/TV99.mp4` and `meta/DRC00.mp4` … `meta/DRC99.mp4`

This is **not** Attract Mode. Attract mode still runs on the normal kiosk UI. Exhibition Mode is toggled under **Kiosk Settings → Set Menu Options → Exhibition Mode**.

---

## What Kiosk Menu expects

When `<nonInteractiveMode>1</nonInteractiveMode>` is set in MenuApp save data, the menu:

1. Scans MCP for title **`000500001FA82700`**
2. Lists that title's `/meta/` directory
3. Keeps files named exactly:
   - `TV00.mp4` … `TV99.mp4` (8 characters)
   - `DRC00.mp4` … `DRC99.mp4` (9 characters)
4. Plays TV clips on HDMI and DRC clips on the GamePad
5. Requires **equal** TV and DRC counts

Wrong names log `ProcessNonInteractiveMovieList(): … is an invalid movie name`. Missing or mismatched counts show **Exhibition Mode is On** with an error string on both screens.

More context: [HowKioskMenuWorks.MD — Exhibition Mode](../HowKioskMenuWorks.MD#exhibition-mode-non-interactive).

---

## Folder layout

```text
1fa82700/
  code/
    exhibition_wrapper.rpx
    app.xml
    cos.xml
  meta/
    meta.xml
    TV00.mp4
    DRC00.mp4
    TV01.mp4
    DRC01.mp4
    ...
```

FTP-ready base folder after build: [`Release/1fa82700/`](../../Release/1fa82700/).

Videos are **not** included in this repo.

---

## Prepare your videos

Use the helper script from this title folder:

```sh
cd "Exhibition Mode"
python3 tools/prepare_videos.py \
  --tv /path/to/tv1.mp4 /path/to/tv2.mp4 \
  --drc /path/to/pad1.mp4 /path/to/pad2.mp4 \
  --out ../Release/1fa82700/meta
```

Or explicit pairs:

```sh
python3 tools/prepare_videos.py \
  --pairs lobby_tv.mp4:lobby_pad.mp4 intro_tv.mp4:intro_pad.mp4 \
  --out ../Release/1fa82700/meta
```

You usually want **different** encodes for TV (1920×1080) and GamePad (854×480), even if the content is the same scene.

### Encode examples

**TV clip:**

```powershell
ffmpeg -y -i "Source.mp4" `
  -map 0:v:0 -map 0:a:0? `
  -c:v libx264 -profile:v high -level 4.0 -pix_fmt yuv420p `
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" `
  -r 30 -c:a aac -b:a 192k -ac 2 -ar 48000 `
  -movflags +faststart -brand mp42 `
  "tv_clip.mp4"
```

**GamePad clip:**

```powershell
ffmpeg -y -i "Source.mp4" `
  -map 0:v:0 -map 0:a:0? `
  -c:v libx264 -profile:v high -level 4.0 -pix_fmt yuv420p `
  -vf "scale=854:480:force_original_aspect_ratio=decrease,pad=854:480:(ow-iw)/2:(oh-ih)/2" `
  -r 30 -c:a aac -b:a 192k -ac 2 -ar 48000 `
  -movflags +faststart -brand mp42 `
  "pad_clip.mp4"
```

Then run `prepare_videos.py` to install them as `TV00.mp4` / `DRC00.mp4`.

---

## Build

```sh
cd "Exhibition Mode"
mkdir -p build && cd build
powerpc-eabi-cmake ..
cmake --build .
```

Build notes: [HowToBuild.MD](../HowToBuild.MD#exhibition-mode--1fa82700).

---

## Install

1. Build the project.
2. Copy your paired videos into `Release/1fa82700/meta/` (use `prepare_videos.py`).
3. FTP `Release/1fa82700/` to `mlc:/usr/title/00050000/1fa82700/`.
4. On the kiosk: **Kiosk Settings → Set Menu Options → Exhibition Mode → On**.
5. Reboot or restart Kiosk Menu.

---

## Troubleshooting

| Issue | Check |
|-------|-------|
| Normal game selector still shows | Exhibition Mode off in save data, or menu not restarted |
| “Exhibition Mode is On” but no video | Title `1fa82700` missing from MLC, or no `TVnn`/`DRCnn` files |
| “Movies … not equal” | Mismatch in TV vs DRC file count |
| “Invalid movie name” | Filename must be exactly `TV00.mp4` or `DRC00.mp4` style |
| Black screen after names fixed | Re-encode with H.264 + AAC, `-movflags +faststart` |

Related:

- [AttractMode.MD](AttractMode.MD)
- [HowKioskMenuWorks.MD](../HowKioskMenuWorks.MD)
