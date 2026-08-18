# Release

FTP-ready title folders. No `content/` on NAND — the kiosk menu reads each catalog from `meta/`.

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

Videos are **not** included in this repo. The kiosk launches the title with argument `0`–`5` to pick a clip.

## Attract Mode — `1fa82100`

```
mlc:/usr/title/00050000/1fa82100/
```

| Path | Files |
|---|---|
| `code/` | `attractmode_wrapper.rpx`, `app.xml`, `cos.xml` |
| `meta/` | `meta.xml`, user videos `AttractMode00.mp4` .. `AttractMode11.mp4` |

Videos are **not** included in this repo. The kiosk launches the title with argument `0`–`11` to pick a clip.

## About Amiibo — `1fa83300`

```
mlc:/usr/title/00050000/1fa83300/
```

| Path | Files |
|---|---|
| `code/` | `aboutamiibo_wrapper.rpx`, `app.xml`, `cos.xml` |
| `meta/` | `meta.xml`, user video `AboutAmiibo00.mp4` |

Video is **not** included in this repo. The kiosk launches the title with argument `0` (single clip).

Rebuilds overwrite the RPX in each `code/` folder.
