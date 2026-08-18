# Attract Mode (`1fa82100`)

Special kiosk helper for idle / attract videos when Kiosk Menu is left alone.

- **Title ID:** `000500001FA82100`
- **MLC path:** `mlc/usr/title/00050000/1fa82100/`
- **RPX:** `attractmode_wrapper.rpx`
- **User files:** `meta/AttractMode00.mp4` ... `meta/AttractMode11.mp4`

This title stores attract-mode clips on MLC. Kiosk Menu scans `meta/` and
builds a rotating playlist (`GetNextAttractModeMovie`); it does not launch the
wrapper RPX for normal attract playback.

---

## What it does

When attract mode is enabled and Kiosk Menu decides to enter the idle movie flow, it reads videos from this title's `meta/` folder.

### How many videos?

This project targets **12 numbered clips** — what known retail kiosk installs use:

```text
AttractMode00.mp4
AttractMode01.mp4
AttractMode02.mp4
AttractMode03.mp4
AttractMode04.mp4
AttractMode05.mp4
AttractMode06.mp4
AttractMode07.mp4
AttractMode08.mp4
AttractMode09.mp4
AttractMode10.mp4
AttractMode11.mp4
```

You do **not** need 100 files. Reverse engineering of retail `MenuApp.rpx` shows:

- Kiosk Menu **scans** `meta/` for filenames starting with `AttractMode`
- It parses a **two-digit index** from each name (e.g. `AttractMode07.mp4` → slot 7)
- It builds a **rotating playlist** and advances with `GetNextAttractModeMovie`, wrapping when it reaches the end
- Decompiled code allocates an internal table with **room for up to 100 slots** — that is a code-side capacity limit, not a retail content count

So in practice: **12 clips on known dumps**, but the menu will pick up any correctly named `AttractModeXX.mp4` files it finds (00–99 by naming). Gaps in the sequence are fine; only present files are played.

If you only want a few videos, keep the naming sequence correct for the files you do provide. Fewer than 12 is untested here but matches how the scanner works.

More context: [HowKioskMenuWorks.MD — Movies and attract mode](../HowKioskMenuWorks.MD#movies-and-attract-mode).

---

## Folder layout

```text
1fa82100/
  code/
    attractmode_wrapper.rpx
    app.xml
    cos.xml
  meta/
    meta.xml
    AttractMode00.mp4
    ...
    AttractMode11.mp4
```

FTP-ready base folder after build: [`Release/1fa82100/`](../../Release/1fa82100/).

Videos are **not** included in this repo.

---

## Encode video

Use the same settings as kiosk trailers and the About Wii U clips:

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
  "AttractMode00.mp4"
```

Re-encode every clip you plan to use.

---

## Build

```sh
cd "Attract Mode"
mkdir -p build && cd build
powerpc-eabi-cmake ..
cmake --build .
```

Build notes: [HowToBuild.MD](../HowToBuild.MD#attract-mode--1fa82100).

---

## Install

1. Build the project.
2. Put your attract-mode videos under `Release/1fa82100/meta/`.
3. Upload `Release/1fa82100/` to `mlc:/usr/title/00050000/1fa82100/`.
4. Reboot or restart Kiosk Menu.

Install tree details: [Release/README.md](../../Release/README.md).

---

## Notes

- This title is only the **movie source** on MLC. Attract-mode timing and playback live in Kiosk Menu.
- Kiosk Menu can have multiple attract-mode styles and settings, but this title's job is just to provide the video files.
- If attract mode looks broken, also check the menu's own settings and not only these MP4s.
- Attract videos are usually without audio. May work with audio.

---

## Troubleshooting

| Issue | Check |
|-------|-------|
| Attract mode never starts | Kiosk Menu settings may disable or change attract mode behavior |
| Attract mode starts but no movie plays | Missing or misnamed `AttractModeXX.mp4` files (`XX` = two-digit slot, e.g. `07`) |
| Some clips work, some do not | Wrong numbering or bad encode on certain files |
| Black screen | Re-encode with H.264 + AAC |

Related:

- [AboutWiiU.MD](AboutWiiU.MD)
- [AboutAmiibo.MD](AboutAmiibo.MD)
- [HowKioskMenuWorks.MD](../HowKioskMenuWorks.MD)
