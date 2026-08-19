# Attract Mode (`1fa82100`)

Special kiosk helper for idle / attract videos when Kiosk Menu is left alone.

- **Title ID:** `000500001FA82100`
- **MLC path:** `mlc/usr/title/00050000/1fa82100/`
- **RPX:** `attractmode_wrapper.rpx`
- **User files:** `meta/AttractMode00.mp4` … `meta/AttractMode11.mp4`

Kiosk Menu scans `meta/` and builds a rotating attract playlist in-menu.

---

## What it does

When attract mode is enabled, Kiosk Menu reads clips from this title's `meta/` folder.

This project targets **12 numbered clips** (known retail kiosk installs):

```text
AttractMode00.mp4
AttractMode01.mp4
...
AttractMode11.mp4
```

Retail `MenuApp.rpx` scans for filenames starting with `AttractMode`, parses a two-digit index, and rotates with `GetNextAttractModeMovie`. 

You do **not** need 100 files but it can support that internally.

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


---

## Encode video

* [ffmpeg](https://ffmpeg.org/download.html) for video.


Use the same settings as other kiosk helper videos:

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

Re-encode every clip you plan to use. Attract videos are usually silent. Audio may still work.

---

## Install

1. Download the latest release from [GitHub Releases](https://github.com/pumpk-bit/Wii-U-Kiosk-Homebrew/releases). Use the `1fa82100/` folder from **All-In-One**.
2. Put `AttractMode00.mp4` … `AttractMode11.mp4` in `meta/` (not included in the release).
3. FTP the folder to `mlc:/usr/title/00050000/1fa82100/`.
4. Reboot the Wii U.

To compile yourself: [HowToBuild.MD](../HowToBuild.MD). 

---

## Troubleshooting

| Issue | Check |
|-------|-------|
| Attract starts but no movie plays | Missing or misnamed `AttractModeXX.mp4` files |
| Some clips work, some do not | Wrong numbering or bad encode on certain files |
| Black screen/One frame | Re-encode with H.264 + AAC |

Related:

- [AboutWiiU.MD](AboutWiiU.MD)
- [Aboutamiibo.MD](Aboutamiibo.MD)
- [HowKioskMenuWorks.MD](../HowKioskMenuWorks.MD)
