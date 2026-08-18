# About Amiibo (`1fa83300`)

Special kiosk helper for the **About amiibo** bubble in Kiosk Menu.

- **Title ID:** `000500001FA83300`
- **MLC path:** `mlc/usr/title/00050000/1fa83300/`
- **RPX:** `aboutamiibo_wrapper.rpx`
- **User file:** `meta/AboutAmiibo00.mp4`

This title stores the About amiibo clip on MLC. Kiosk Menu scans `meta/` and
plays it in-menu; it may also launch this wrapper with argument `0` in some
configurations.

---

## What it does

Kiosk Menu uses this title for the **About amiibo** screen / button.

This expects a single clip:

```text
AboutAmiibo00.mp4
```

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

FTP-ready base folder after build: [`Release/1fa83300/`](../../Release/1fa83300/).

Video is **not** included in this repo.

---

## Encode video

Use the same encoding rules as the kiosk trailers and other helper-video titles:

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

## Build

```sh
cd "About Amiibo"
mkdir -p build && cd build
powerpc-eabi-cmake ..
cmake --build .
```

Build notes: [HowToBuild.MD](../HowToBuild.MD#about-amiibo--1fa83300).

---

## Install

1. Build the project.
2. Put your video at `Release/1fa83300/meta/AboutAmiibo00.mp4`.
3. Upload `Release/1fa83300/` to `mlc:/usr/title/00050000/1fa83300/`.
4. Reboot or restart Kiosk Menu.

Install tree details: [Release/README.md](../../Release/README.md).

---

## Notes

- This title is separate from Kiosk Menu text and button labels.
- The menu UI decides when to show the About amiibo entry; this title only supplies the playable clip.

---

## Troubleshooting

| Issue | Check |
|-------|-------|
| About amiibo button does nothing | Missing `AboutAmiibo00.mp4` or bad install path |
| Black screen/one frame | Re-encode the MP4 |
| Bubble missing in Kiosk Menu | The title is missing or the menu build does not expose that entry |

Related:

- [AboutWiiU.MD](AboutWiiU.MD)
- [AttractMode.MD](AttractMode.MD)
- [HowKioskMenuWorks.MD](../HowKioskMenuWorks.MD)
