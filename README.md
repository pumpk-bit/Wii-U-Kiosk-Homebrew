# Wii U Kiosk Homebrew

Replacement apps for Wii U kiosk. These are new homebrew versions of these apps, not Nintendo code or assets.

Smaller in size and open source.

| App | Title ID | Tutorial | Release folder | Notes |
|---|---|---|---|---|
| Featured List | `000500001FA82200` | [FeaturedList.MD](docs/Title/FeaturedList.MD) | `Release/1fa82200/` | Tells kiosk menu what titles are "featured".|
| New Releases | `000500001FA82300` | [NewReleases.MD](docs/Title/NewReleases.MD) | `Release/1fa82300/` | Tells kiosk menu what titles are "new".|
| About Wii U | `000500001FA82000` | [AboutWiiU.MD](docs/Title/AboutWiiU.MD) | `Release/1fa82000/` | Opens a bubble on the right with Wii U explainer videos (`meta/`). |
| Attract Mode | `000500001FA82100` | [AttractMode.MD](docs/Title/AttractMode.MD) | `Release/1fa82100/` | Idle attract videos (`meta/`). |
| About Amiibo | `000500001FA83300` | [Aboutamiibo.MD](docs/Title/Aboutamiibo.MD) | `Release/1fa83300/` | Opens a bubble on the left with an Amiibo video (`meta/`). |

Note: titles may show up as "???" on the Wii U. Do not delete them. No `content/` folder is required.

For reverse-engineering notes on how the retail kiosk menu uses these titles, see [HowKioskMenuWorks.MD](docs/HowKioskMenuWorks.MD).

## How to build

Needs [devkitPro](https://devkitpro.org/) **wiiu-dev**, **CMake**, and **Python 3.8+**. Full first-time install: [HowToBuild.MD](docs/HowToBuild.MD).

Windows (MSYS2 — stock PowerShell cannot compile):

```powershell
powershell -File tools/launch-msys2-wiiu.ps1
```

then in that shell:

```sh
bash tools/check-toolchain.sh
bash tools/build-all.sh
```

Linux / macOS:

```sh
bash tools/check-toolchain.sh
bash tools/build-all.sh
```

## How to install (FTP)

Please read the tutorial first before copying.

Copy a `Release/<unique-id>/` folder to `mlc:/usr/title/00050000/<unique-id>/`.

Example:

* Featured List

Copy the folder over:

```
mlc:/usr/title/00050000/1fa82200/
```

Make sure the files are there:

```
mlc:/usr/title/00050000/1fa82200/code/  Should contain: app.xml  cos.xml  title_list.rpx
mlc:/usr/title/00050000/1fa82200/meta/  Should contain: Featured.xml  meta.xml
```


## What is not in this repo

Nintendo dumps, boot screens, original RPX binaries, and Ghidra output stay out of git. Keep those in `SourceCD/` (gitignored). See `SourceCD/README.md`.


## Thanks to

Thanks: [Ghidra](https://github.com/NationalSecurityAgency/ghidra/releases), [GhidraRPXLoader](https://github.com/Maschell/GhidraRPXLoader), and Cursor AI ([cursor.com](https://cursor.com/))

## AI

Cursor AI was used to help in this project. Cursor helped fix spelling and make code for the project.