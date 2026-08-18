# Build

Requires [devkitPro](https://devkitpro.org/) with **wiiu-dev** (that pulls in **wut** and **devkitPPC**), plus **CMake** and **Python 3.8+**.

No machine-specific paths are required. If `DEVKITPRO` is already set (the official installer does this), the scripts use it. Otherwise they look in the usual places (`C:\devkitPro`, `/opt/devkitpro`). Current toolchains keep `powerpc-eabi-cmake` in `$DEVKITPRO/portlibs/wiiu/bin`; `tools/env.sh` adds that folder to `PATH`.

Each project copies its RPX into [`Release/<id>/code/`](../Release/) and runs `tools/generate_title_xml.py` into the same `Release/<id>/` tree. A `.wuhb` is built only if `wuhbtool` is present. Kiosk FTP does not need it.

Videos are **not** in this repo. Add your own MP4s under `Release/<id>/meta/` after building.

---

## 1. Install tools (once)

### Windows

1. Install [Git](https://git-scm.com/download/win) and [Python 3](https://www.python.org/downloads/) (tick **Add python.exe to PATH**).
2. Install [devkitPro](https://devkitpro.org/wiki/Getting_Started) with the Windows installer.
3. Open the **MSYS2** shell it created (Start menu → devkitPro → MSYS) and install the Wii U group:

```sh
pacman -Syu --needed wiiu-dev cmake python
```

4. Clone this repository.

### Linux or macOS

1. Install **Git**, **Python 3**, and **CMake** from your OS (`python3`, `cmake`).
2. Install [devkitPro pacman](https://devkitpro.org/wiki/Getting_Started), then:

```sh
sudo dkp-pacman -Syu --needed wiiu-dev
```

3. Clone this repository. Log out and back in (or `source /etc/profile.d/devkit-env.sh`) so `DEVKITPRO` is set.

---

## 2. Open a build shell

**Windows:** stock PowerShell cannot run `powerpc-eabi-cmake`. Open MSYS2 in this repo:

```powershell
powershell -File tools/launch-msys2-wiiu.ps1
```

**Linux / macOS:** use a normal terminal in the repo.

The other scripts call `source tools/env.sh` themselves. You do not have to set `PATH` by hand.

---

## 3. Check the toolchain

```sh
bash tools/check-toolchain.sh
```

Windows shortcut (uses bash if Git Bash / MSYS2 is on `PATH`):

```powershell
powershell -File tools/check-toolchain.ps1
```

---

## 4. Build everything

From a shell that has `powerpc-eabi-cmake` (the MSYS2 window, or Linux/macOS after step 2):

```sh
bash tools/build-all.sh
```

Or one title:

```sh
bash tools/build-all.sh "Featured List"
```

Windows shortcut (needs Git Bash or MSYS2 `bash`):

```powershell
powershell -File tools/build-all.ps1
```

Output: `Release/<unique-id>/`. Then FTP as in [Release/README.md](../Release/README.md).

Generate XML only (no C compiler):

```sh
python3 tools/generate_title_xml.py
python3 tools/generate_title_xml.py featured
```

Featured / New Releases catalog files are created once. Re-running the generator will not overwrite your edited `Featured.xml` / `NewReleases.xml`.

---

## Featured List — `1fa82200`

From the repo root, after the toolchain check:

```sh
cd "Featured List"
mkdir -p build && cd build
powerpc-eabi-cmake ..
cmake --build .
```

`cmake --build` copies the RPX and writes Cafe XML when Python is on `PATH`. Output: `Release/1fa82200/` — see [Title/FeaturedList.MD](Title/FeaturedList.MD).

---

## New Releases — `1fa82300`

From the repo root, after the toolchain check:

```sh
cd "New Releases"
mkdir -p build && cd build
powerpc-eabi-cmake ..
cmake --build .
```

Output: `Release/1fa82300/` — see [Title/NewReleases.MD](Title/NewReleases.MD).

---

## About Wii U — `1fa82000`

From the repo root, after the toolchain check:

```sh
cd "About Wii U"
mkdir -p build && cd build
powerpc-eabi-cmake ..
cmake --build .
```

Add your own `AboutWiiU00.mp4` … `AboutWiiU05.mp4` under `Release/1fa82000/meta/` before FTP.

---

## Attract Mode — `1fa82100`

From the repo root, after the toolchain check:

```sh
cd "Attract Mode"
mkdir -p build && cd build
powerpc-eabi-cmake ..
cmake --build .
```

Add `AttractMode00.mp4` … `AttractMode11.mp4` under `Release/1fa82100/meta/`.

---

## About Amiibo — `1fa83300`

From the repo root, after the toolchain check:

```sh
cd "About Amiibo"
mkdir -p build && cd build
powerpc-eabi-cmake ..
cmake --build .
```

Add `AboutAmiibo00.mp4` under `Release/1fa83300/meta/`.

---

## FTP install

See [Release/README.md](../Release/README.md) for per-title file lists and `mlc:/usr/title/00050000/<id>/` paths.
