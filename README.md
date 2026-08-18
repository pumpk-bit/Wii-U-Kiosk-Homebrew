# Wii U Kiosk Homebrew

Replacement apps for Wii U kiosk. These are new homebrew versions of these apps, not Nintendo code or assets.

Smaller in size and open source.

| App | Title ID | Tutorial | Release folder | Notes |
|---|---|---|---|---|
| Featured List | `000500001FA82200` | [FeaturedList.MD](docs/Title/FeaturedList.MD) | `Release/1fa82200/` | Tells kiosk menu what titles are "featured". |
| New Releases | `000500001FA82300` | [NewReleases.MD](docs/Title/NewReleases.MD) | `Release/1fa82300/` | Tells kiosk menu what titles are "new".|
| About Wii U | `000500001FA82000` | [AboutWiiU.MD](docs/Title/AboutWiiU.MD) | `Release/1fa82000/` | About Wii U bubble (right side of game selector); videos in `meta/`. |
| Attract Mode | `000500001FA82100` | [AttractMode.MD](docs/Title/AttractMode.MD) | `Release/1fa82100/` | Idle attract videos (`meta/`). |
| About Amiibo | `000500001FA83300` | [AboutAmiibo.MD](docs/Title/Aboutamiibo.MD) | `Release/1fa83300/` | About amiibo bubble (left side of game selector); video in `meta/`. |
| Exhibition Mode | `000500001FA82700` | [ExhibitionMode.MD](docs/Title/ExhibitionMode.MD) | `Release/1fa82700/` | Dual-screen movie loop when Exhibition Mode is enabled (`meta/TVnn.mp4` + `DRCnn.mp4`). |

Note: titles may show up as "???" on the Wii U. Do not delete them. No `content/` folder is required.

For reverse-engineering notes on how the retail kiosk menu uses these titles, see [HowKioskMenuWorks.MD](docs/HowKioskMenuWorks.MD).


## How to install (FTP)

Read the tutorial for each title before copying files.

1. Download the latest release from [GitHub Releases](https://github.com/pumpk-bit/Wii-U-Kiosk-Homebrew/releases). **All-In-One** includes every pre-built title folder.
2. Customize `meta/` if needed (demo lists, videos — not included in the release).
3. FTP each `1fa8xxxx/` folder to `mlc:/usr/title/00050000/<unique-id>/`.
4. Reboot or restart Kiosk Menu.

Example — **Featured List**:

```
mlc:/usr/title/00050000/1fa82200/
  code/   app.xml  cos.xml  title_list.rpx
  meta/   Featured.xml  meta.xml
```

Per-title steps: see the **Tutorial** column above. File checklist: [Release/README.md](Release/README.md).

To compile from source instead: [HowToBuild.MD](docs/HowToBuild.MD).

## How to build

Needs [devkitPro](https://devkitpro.org/) **wiiu-dev (wut)**, **CMake**, and **Python 3.8+**. Full first-time install: [HowToBuild.MD](docs/HowToBuild.MD).

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


## What is not in this repo

Nintendo dumps, original RPX binaries, and Ghidra outputs.


## Thanks to

Thanks: [Ghidra](https://github.com/NationalSecurityAgency/ghidra/releases), [GhidraRPXLoader](https://github.com/Maschell/GhidraRPXLoader), and Cursor AI ([cursor.com](https://cursor.com/))

## AI

Cursor AI was used to help in this project. Cursor helped fix docs and make code for the project.
