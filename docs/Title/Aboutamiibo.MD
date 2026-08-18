# About Amiibo (`1fa83300`)

Special kiosk helper for the **About amiibo** bubble in Kiosk Menu.

- **Title ID:** `000500001FA83300`
- **MLC path:** `mlc/usr/title/00050000/1fa83300/`
- **RPX:** `aboutamiibo_wrapper.rpx`
- **User file:** `meta/AboutAmiibo00.mp4`

Kiosk Menu scans `meta/` and plays the clip in-menu.

---

## What it does

This title supplies the **About amiibo** video. Kiosk Menu expects one file:

```text
AboutAmiibo00.mp4
```

Button labels live in Kiosk Menu itself.

---

## Folder layout

```text
1fa83300/
  code/
    aboutamiibo_wrapper.rpx
    app.xml
    cos.xml
  meta/
    meta.xml
    AboutAmiibo00.mp4
```

Pre-built in releases: `1fa83300/` inside [All-In-One](../../Release/All-In-One/). Video is **not** included.

---

## Encode video

Use the same encoding rules as other kiosk helper videos:

```powershell
ffmpeg -y -i "YourSource.mp4" `
  -map 0:v:0 -map 0:a:0? `
  -c:v libx264 -profile:v high -level 4.0 -pix_fmt yuv420p `
  -x264-params "cabac=1:ref=4:deblock=1:0:0:me=hex:subme=7" `
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" `
  -r 30 `
  -c:a aac -b:a 192k -ac 2 -ar 48000 `
  -movflags +faststart `
  -brand mp42 `
  "AboutAmiibo00.mp4"
```

---

## Install

1. Download the latest release from [GitHub Releases](https://github.com/pumpk-bit/Wii-U-Kiosk-Homebrew/releases). Use the `1fa83300/` folder from **All-In-One**.
2. Put `AboutAmiibo00.mp4` in `meta/` (not included in the release).
3. FTP the folder to `mlc:/usr/title/00050000/1fa83300/`.
4. Reboot or restart Kiosk Menu.

To compile yourself: [HowToBuild.MD](../HowToBuild.MD). File checklist: [Release/README.md](../../Release/README.md).

---

## Troubleshooting

| Issue | Check |
|-------|-------|
| About amiibo button does nothing | Missing `AboutAmiibo00.mp4` or bad install path |
| Black screen / one frame | Re-encode the MP4 |
| Bubble missing in Kiosk Menu | Title not installed on MLC |

Related:

- [AboutWiiU.MD](AboutWiiU.MD)
- [AttractMode.MD](AttractMode.MD)
- [HowKioskMenuWorks.MD](../HowKioskMenuWorks.MD)
