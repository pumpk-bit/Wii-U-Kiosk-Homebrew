# About Wii U (`1fa82000`)

Special kiosk helper for the **About Wii U** bubble in Kiosk Menu.

- **Title ID:** `000500001FA82000`
- **MLC path:** `mlc/usr/title/00050000/1fa82000/`
- **RPX:** `aboutwiiu_wrapper.rpx`
- **User files:** `meta/AboutWiiU00.mp4` … `meta/AboutWiiU05.mp4`

Kiosk Menu scans `meta/` and plays the six About Wii U clips in-menu.

---

## What it does

| Slot | Typical subject |
|------|------------------|
| `00` | What is Wii U? |
| `01` | Wii U GamePad |
| `02` | Miiverse |
| `03` | Expanded |
| `04` | eShop |
| `05` | Accessories |

Button labels live in Kiosk Menu itself. This title only needs the matching MP4 files in `meta/`.

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


Use these exact filenames, wrong names mean a button may not find its clip.

---

## Encode video

* [ffmpeg](https://ffmpeg.org/download.html) for video.


- **1920×1080**, H.264 High@L4.0, AAC stereo 48 kHz, `.mp4` container

Example (repeat for slots `00`–`05`):

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

---

## Install

1. Download the latest release from [GitHub Releases](https://github.com/pumpk-bit/Wii-U-Kiosk-Homebrew/releases). Use the `1fa82000/` folder from **All-In-One**.
2. Put `AboutWiiU00.mp4` … `AboutWiiU05.mp4` in `meta/` (not included in the release).
3. FTP the folder to `mlc:/usr/title/00050000/1fa82000/`.
4. Reboot the Wii U.

To compile yourself: [HowToBuild.MD](../HowToBuild.MD).

---

## Troubleshooting

| Issue | Check |
|-------|-------|
| Button opens but no video plays | Missing or misnamed file (e.g. `AboutWiiU03.mp4`) |
| Black screen during playback / one frame | Re-encode to kiosk-friendly H.264 + AAC |
| Only some buttons work | Not all six files are present |
| Bubble missing in Kiosk Menu | Title not installed on MLC |

Related:

- [AttractMode.MD](AttractMode.MD)
- [Aboutamiibo.MD](Aboutamiibo.MD)
- [HowKioskMenuWorks.MD](../HowKioskMenuWorks.MD)
