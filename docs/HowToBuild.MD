# Build

Requires [devkitPro](https://devkitpro.org/) with **wiiu-dev** (**wut**, **devkitPPC**), plus **CMake** and **Python 3.8+**.

If `DEVKITPRO` is already set in the system variables (the official installer does this), the scripts use it. Otherwise they look in the usual places (`C:\devkitPro`, `/opt/devkitpro`). Current toolchains keep `powerpc-eabi-cmake` in `$DEVKITPRO/portlibs/wiiu/bin`; `tools/env.sh` adds that folder to `PATH`.

Each project copies its RPX into [`Release/<id>/code/`](../Release/) and runs `tools/generate_title_xml.py` into the same `Release/<id>/` tree. A `.wuhb` is built only if `wuhbtool` is present. Kiosk does not use `.whub` and only `.rpx`.

Videos are **not** in this repo. Add your own MP4s under `Release/<id>/meta/` after building.

---

## 1. Install tools (once)

1. Install [Python 3](https://www.python.org/downloads/).
2. Install [devkitPro](https://devkitpro.org/wiki/Getting_Started) and Wii U tools.

---

## 2. Open a build shell

Open MSYS2 in this repo:

```powershell
powershell -File tools/launch-msys2-wiiu.ps1
```

The other scripts call `source tools/env.sh` themselves. You do not have to set `PATH` by hand.

---

## 3. Check the toolchain

```sh
bash tools/check-toolchain.sh
```


---

## 4. Build everything

From MSYS2 window:

```sh
bash tools/build-all.sh
```

Or one title:

```sh
bash tools/build-all.sh "Featured List"
```

Output: `Release/<unique-id>/`. Then FTP as in [Release/README.md](../Release/README.md).

Generate XML only (no C compiler):

```sh
python3 tools/generate_title_xml.py
python3 tools/generate_title_xml.py featured
```

Featured / New Releases catalog files are created once. Re-running the generator will not overwrite your edited `Featured.xml` / `NewReleases.xml`.

---

## Featured List  `1fa82200`

From the repo root, after the toolchain check:

```sh
cd "Featured List"
mkdir -p build && cd build
powerpc-eabi-cmake ..
cmake --build .
```

`cmake --build` copies the RPX and writes Cafe XML when Python is on `PATH`. Output: `Release/1fa82200/` — see [Title/FeaturedList.MD](Title/FeaturedList.MD).

---

## New Releases `1fa82300`

From the repo root, after the toolchain check:

```sh
cd "New Releases"
mkdir -p build && cd build
powerpc-eabi-cmake ..
cmake --build .
```

Output: `Release/1fa82300/`, see [Title/NewReleases.MD](Title/NewReleases.MD).

---

## About Wii U `1fa82000`

From the repo root, after the toolchain check:

```sh
cd "About Wii U"
mkdir -p build && cd build
powerpc-eabi-cmake ..
cmake --build .
```

Add your own `AboutWiiU00.mp4` … `AboutWiiU05.mp4` under `Release/1fa82000/meta/` before FTP.

---

## Attract Mode `1fa82100`

From the repo root, after the toolchain check:

```sh
cd "Attract Mode"
mkdir -p build && cd build
powerpc-eabi-cmake ..
cmake --build .
```

Add `AttractMode00.mp4` … `AttractMode11.mp4` under `Release/1fa82100/meta/`.

---

## About Amiibo `1fa83300`

From the repo root, after the toolchain check:

```sh
cd "About Amiibo"
mkdir -p build && cd build
powerpc-eabi-cmake ..
cmake --build .
```

Add `AboutAmiibo00.mp4` under `Release/1fa83300/meta/`.

---

## Exhibition Mode `1fa82700`

From the repo root, after the toolchain check:

```sh
cd "Exhibition Mode"
mkdir -p build && cd build
powerpc-eabi-cmake ..
cmake --build .
```

Make sure videos are formated with what the kiosk expects. The tool only renames them and copies over them. If you only plan on using few videos then you can rename them by hand.

* [ffmpeg](https://ffmpeg.org/download.html) for video encoding.

Add paired `TV00.mp4` / `DRC00.mp4` … under `Release/1fa82700/meta/`. From the
`Exhibition Mode/` folder (not `build/`):

```sh
cd ..
python3 tools/prepare_videos.py --tv ... --drc ... --out ../Release/1fa82700/meta
```

Or from the repo root:

```sh
python3 "Exhibition Mode/tools/prepare_videos.py" --tv ... --drc ... --out Release/1fa82700/meta
```

Enable **Exhibition Mode** in Kiosk Menu maintenance settings after FTP.


---

## FTP install

See [Release/README.md](../Release/README.md) for per-title file lists and `mlc:/usr/title/00050000/<id>/` paths.
