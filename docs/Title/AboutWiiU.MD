# About Wii U (`1fa82000`)

Special kiosk helper for the **About Wii U** bubble in Kiosk Menu.

- **Title ID:** `000500001FA82000`
- **MLC path:** `mlc/usr/title/00050000/1fa82000/`
- **RPX:** `aboutwiiu_wrapper.rpx`
- **User files:** `meta/AboutWiiU00.mp4` ... `meta/AboutWiiU05.mp4`

This title stores the six About Wii U clips on MLC. Kiosk Menu scans `meta/`
and plays them in-menu; it may also launch this wrapper with a slot index in
some configurations.

---

## What it does

Kiosk Menu uses this title for the six **About Wii U** videos:

| Slot | Typical subject |
|------|------------------|
| `00` | What is Wii U? |
| `01` | Wii U GamePad |
| `02` | Miiverse |
| `03` | Expanded |
| `04` | eShop |
| `05` | Accessories |

The exact button text lives in Kiosk Menu itself. This title just needs the matching MP4 files in `meta/`.

---

## Folder layout

```text
1fa82000/
  code/
    aboutwiiu_wrapper.rpx
    app.xml
    cos.xml
  meta/
    meta.xml
    AboutWiiU00.mp4
    AboutWiiU01.mp4
    AboutWiiU02.mp4
    AboutWiiU03.mp4
    AboutWiiU04.mp4
    AboutWiiU05.mp4
```

FTP-ready base folder after build: [`Release/1fa82000/`](../../Release/1fa82000/).

Videos are **not** included in this repo.

---

## Video naming

Use these exact filenames:

```text
AboutWiiU00.mp4
AboutWiiU01.mp4
AboutWiiU02.mp4
AboutWiiU03.mp4
AboutWiiU04.mp4
AboutWiiU05.mp4
```

The wrapper and kiosk menu expect this naming pattern. Wrong names mean the button may do nothing or fail to find the movie.

---

## Encode video

Use the same encoding style as kiosk demo trailers:

- **1920x1080**
- **H.264 High@L4.0**
- **AAC stereo 48 kHz**
- `.mp4` container

Example:

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
  "AboutWiiU00.mp4"
```

Repeat for the other slots.

---

## Build

```sh
cd "About Wii U"
mkdir -p build && cd build
powerpc-eabi-cmake ..
cmake --build .
```

Build notes: [HowToBuild.MD](../HowToBuild.MD#about-wii-u--1fa82000).

---

## Install

1. Build the project.
2. Put your videos under `Release/1fa82000/meta/`.
3. Upload `Release/1fa82000/` to `mlc:/usr/title/00050000/1fa82000/`.
4. Reboot or restart Kiosk Menu.

See also: [Release/README.md](../../Release/README.md).

---

## Troubleshooting

| Issue | Check |
|-------|-------|
| About Wii U button opens but no video plays | Missing or misnamed file (e.g. `AboutWiiU03.mp4`) |
| Black screen during playback | Re-encode the MP4 to kiosk-friendly H.264 + AAC |
| Only some buttons work | You only added some of the six files |
| Bubble missing in Kiosk Menu | This title is not installed on MLC |

Related:

- [AttractMode.MD](AttractMode.MD)
- [AboutAmiibo.MD](AboutAmiibo.MD)
- [HowKioskMenuWorks.MD](../HowKioskMenuWorks.MD)
