# Release

Per-title FTP layout. Run `bash tools/build-all.sh` first — checked-in folders
contain XML only until you compile; rebuilds copy each RPX into `code/`. No
`content/` on NAND — the kiosk menu reads catalogs and videos from `meta/`.

## Featured List — `1fa82200`

```
mlc:/usr/title/00050000/1fa82200/
```

| Path | Files |
|---|---|
| `code/` | `title_list.rpx`, `app.xml`, `cos.xml` |
| `meta/` | `Featured.xml`, `meta.xml` |

## New Releases — `1fa82300`

```
mlc:/usr/title/00050000/1fa82300/
```

| Path | Files |
|---|---|
| `code/` | `newreleases_wrapper.rpx`, `app.xml`, `cos.xml` |
| `meta/` | `NewReleases.xml`, `meta.xml` |

## About Wii U — `1fa82000`

```
mlc:/usr/title/00050000/1fa82000/
```

| Path | Files |
|---|---|
| `code/` | `aboutwiiu_wrapper.rpx`, `app.xml`, `cos.xml` |
| `meta/` | `meta.xml`, user videos `AboutWiiU00.mp4` .. `AboutWiiU05.mp4` |

Videos are **not** included in this repo. Kiosk Menu scans `meta/` and plays
clips in-menu; it may also launch this wrapper with argument `0`–`5` in some
configurations.

## Attract Mode — `1fa82100`

```
mlc:/usr/title/00050000/1fa82100/
```

| Path | Files |
|---|---|
| `code/` | `attractmode_wrapper.rpx`, `app.xml`, `cos.xml` |
| `meta/` | `meta.xml`, user videos `AttractMode00.mp4` .. `AttractMode11.mp4` |

Videos are **not** included in this repo. Kiosk Menu scans `meta/` and rotates
through the playlist in-menu; it does not launch the wrapper RPX for normal
attract playback.

## About Amiibo — `1fa83300`

```
mlc:/usr/title/00050000/1fa83300/
```

| Path | Files |
|---|---|
| `code/` | `aboutamiibo_wrapper.rpx`, `app.xml`, `cos.xml` |
| `meta/` | `meta.xml`, user video `AboutAmiibo00.mp4` |

Video is **not** included in this repo. Kiosk Menu scans `meta/` and plays the
clip in-menu; it may also launch this wrapper with argument `0` in some
configurations.

## Exhibition Mode — `1fa82700`

```
mlc:/usr/title/00050000/1fa82700/
```

| Path | Files |
|---|---|
| `code/` | `exhibition_wrapper.rpx`, `app.xml`, `cos.xml` |
| `meta/` | `meta.xml`, user videos `TV00.mp4` + `DRC00.mp4` … (paired, equal count) |

Videos are **not** included. Kiosk Menu reads these files directly when **Exhibition Mode** is enabled in maintenance settings; it does not launch the wrapper RPX for playback.

