# How Kiosk Menu Works

Best-effort reverse engineering of the retail Wii U kiosk menu (`00050010-1FA81000`). This explains what **MenuApp.rpx** does so homebrew helper titles in this repo can match real behavior.

**Sources:** extracted title files, Ghidra decompilation of `MenuApp.rpx` / `mvplayer.rpl` / `SESClient.rpl`, and runtime string hits from an emulator memory dump. All code in this project was remade without copying from the dumps.

**On this page**

- [At a glance](#at-a-glance)
- [Related helper titles](#related-helper-titles)
- [What is inside the menu title](#what-is-inside-the-menu-title)
- [Three-layer architecture](#three-layer-architecture)
- [Startup and main loop](#startup-and-main-loop)
- [Region and UI strings](#region-and-ui-strings)
- [Screens and navigation](#screens-and-navigation)
- [Demo catalog and KioskMeta.xml](#demo-catalog-and-kioskmetaxml)
- [Featured, New, and Active lists](#featured-new-and-active-lists)
- [Movies and attract mode](#movies-and-attract-mode)
- [Launching games and demos](#launching-games-and-demos)
- [SES and fleet management](#ses-and-fleet-management)
- [Media playback (`mvplayer.rpl`)](#media-playback-mvplayerrpl)
- [Confidence levels](#confidence-levels)
- [Still unknown](#still-unknown)

---

## At a glance

| | |
|--|--|
| Title ID | `00050010-1FA81000` |
| English name | Kiosk Menu |
| Product code | `WUP-N-HB2A` (retail kiosk build) |
| MLC path | `mlc/sys/title/00050010/1fa81000/` |
| Main binary | `MenuApp.rpx` (`cos.xml` → `argstr`) |
| Companion libraries | `mvplayer.rpl`, `SESClient.rpl` |
| Build string seen at runtime | `Wii U Interactive Menu - revision 890` |

The kiosk menu is **not** a thin launcher. It owns the application loop, UI screens, movie playback, title filtering, launch policy (ratings, accessories), and communication with Nintendo's kiosk service layer (SES).

---

## Related helper titles

MenuApp hard-codes several companion title IDs and treats each one specially. This repo ships open-source replacements for the video/list helpers:

| ID | Role | Homebrew doc |
|----|------|--------------|
| `000500001FA82200` | Featured demo list (`meta/Featured.xml`) | [FeaturedList.MD](Title/FeaturedList.MD) |
| `000500001FA82300` | New releases list (`meta/NewReleases.xml`) | [NewReleases.MD](Title/NewReleases.MD) |
| `000500001FA82000` | About Wii U videos | [AboutWiiU.MD](Title/AboutWiiU.MD) |
| `000500001FA82100` | Attract mode playlist | [AttractMode.MD](Title/AttractMode.MD) |
| `000500001FA83300` | About Amiibo video | [Aboutamiibo.MD](Title/Aboutamiibo.MD) |
| `000500001FA82400` | Active list wrapper (retail only; not in this repo) | — |

Demo tiles themselves live under `mlc/usr/title/00050002/<id>/` and carry `meta/KioskMeta.xml`.

---

## What is inside the menu title

Typical layout under `1fa81000/`:

```text
code/
  MenuApp.rpx
  mvplayer.rpl
  SESClient.rpl
  app.xml
  cos.xml
  title.fst
  title.tmd
meta/
  meta.xml
content/menuapp/
  MenuConfiguration/
    MessageStudio.xml
    DefaultMenuConfigurationnoa.xml
    DefaultMenuConfigurationnoe.xml
    DefaultMenuConfigurationncl.xml
  fonts/*.fnt
```

At runtime the menu reads config from paths like:

- `/vol/content/MenuApp/MenuConfiguration/MessageStudio.xml`
- `/vol/content/MenuApp/MenuConfiguration/DefaultMenuConfigurationNOA.xml` (and NOE / NCL variants)

Important `meta.xml` flags include `app_launch_type = 00000001`, `launching_flag = 00000004`, `bg_daemon_enable = 1`, and `drc_use = 1`.

---

## Three-layer architecture

Decompilation points to three cooperating binaries in `code/`:

```text
MenuApp.rpx          UI, screens, title list, launch handoff, SES requests
       │
       ├── mvplayer.rpl    decode/render local or streamed video (H.264 + AAC)
       │
       └── SESClient.rpl   BOSS/network, install state, heartbeat, title reconciliation
```

| Layer | Responsibility |
|-------|----------------|
| **MenuApp.rpx** | Main loop, screen classes, curated title list, movie selection, deferred launch intent, XML request builders for featured/new/active |
| **mvplayer.rpl** | Media backend: H.264/AAC decode, TV and GamePad output, seek/pause/buffer, local files and HTTP/HLS |
| **SESClient.rpl** | Persistent XML state, account/auth, polling, installed-title reconciliation, install/delete/reboot windows |

---

## Startup and main loop

`main()` is a real application loop, not a one-shot launcher.

Startup roughly:

1. Initialize low-level systems and `CafeMenuPatchClass`
2. Start waiting for title-list updates
3. Initialize `SESClass` and USB handling
4. Initialize TV + GamePad graphics and `Draw2DClass`
5. Enter the menu loop

Each frame the loop updates rendering, input, language changes, SES communication, watchdogs, and auto-restart logic.

On exit:

1. `MenuScreenLaunchGameClass` is queried for launch title ID, launch path, inactivity-timer override, and system-updater flag
2. Movie playback stops via `MoviePlayerClass::StopMovie`
3. `CafeMenuPatchClass::LaunchTitle()` performs the handoff

The screen layer decides **what** to launch; `CafeMenuPatchClass` performs the actual launch.

Named subsystems visible in symbols:

- `CafeMenuPatchClass` — title management and launch
- `MenuConfigurationClass` — region config and movie-list discovery
- `MoviePlayerClass` — in-menu playback facade
- `SESClass` — high-level service requests
- `AutoRestartClass` — kiosk watchdog behavior
- Screen classes: `MenuScreenGameSelectorClass`, `MenuScreenCategorySelectorClass`, `MenuScreenAboutWiiUClass`, `MenuScreenAboutAmiiboClass`, `MenuScreenLaunchGameClass`, `MenuScreenMoviePlayerClass`, `MenuScreenNonInteractiveModeClass`, maintenance-mode screens

---

## Region and UI strings

### Region presets

Three small XML files under `content/menuapp/MenuConfiguration/`:

| File | Region | Language | Rating board |
|------|--------|----------|--------------|
| `DefaultMenuConfigurationnoa.xml` | NOA | `US_English` | ESRB |
| `DefaultMenuConfigurationnoe.xml` | NOE | `EU_English` | PEGI_EU |
| `DefaultMenuConfigurationncl.xml` | NCL | `JP_Japanese` | CERO |

Startup flow appears to be: pick regional preset → load matching defaults → choose language/rating variants from the message database. Region behavior is **data-driven**.

### MessageStudio.xml

Almost all readable UI text lives in `MessageStudio.xml`:

- Screen and button labels
- Translator comments (often name screen codes like `B3`, `D1`…`D6`)
- Per-region/per-language variants and old text history
- Hints about screen behavior

It describes **UI and flow**, not the per-demo title database. Demo presentation comes from each title's `KioskMeta.xml`.

---

## Screens and navigation

### Top-level game selector

String keys confirm curated rows plus genre groupings:

- Featured Titles, New Releases
- Adventure/RPG, Action/Shooter, Board/Puzzle, Sports/Racing, Music/Health
- All Titles

The carousel is not one flat list — it mixes curated rows, genre entry points, and a catch-all view.

### Action buttons per title

| String key | English label | Notes |
|------------|---------------|-------|
| `drc_btn_game_selector_play_demo` | Play Demo | Standard demo launch |
| `drc_btn_game_selector_play_game` | Play Game | Full-game kiosk units only |
| `drc_btn_game_selector_video` | Video | Full-screen trailer toggle |
| `drc_btn_game_selector_more_selections` | More Categories | Opens category browser |
| `drc_btn_game_selector_about_wiiu` | About Wii U | |
| `drc_btn_game_selector_about_amiibo` | About amiibo | |

Translator comments map these to screen codes (`B3`, `B3a`, `B4`, etc.).

### Category browser

Finer genre labels include action, adventure, rpg, puzzle, sports, music, fighting, education, and others. The RPX contains `MenuScreenCategorySelectorClass` with dedicated touch/run/draw handlers — category browsing is a real screen, not leftover strings.

### About Wii U layout

Six named video buttons in MessageStudio (`drc_btn_about_wiiu_vid01` … `vid06`), with labels such as:

- What is Wii U?
- Wii U GamePad
- Miiverse
- Expanded
- eShop
- Accessories

These map to `AboutWiiU00.mp4` … `AboutWiiU05.mp4` in the About Wii U helper title's `meta/` folder.

### Kiosk settings (maintenance)

Runtime strings confirm editable kiosk fields:

- `kioskID`
- `attractModeMode`
- `nonInteractiveMode`

Maintenance screens include kiosk ID editing and attract-mode mode selection.

---

## Demo catalog and KioskMeta.xml

### How the title list is built

`CafeMenuPatchClass` does **not** show a raw MCP title list. The pipeline:

1. Call MCP for the system title list
2. Optionally merge an Active list from title `000500001FA82400`
3. Reject some entries if a retail metadata wrapper is present
4. Run each title through `ProcessSpecialTitleID`
5. Optionally filter with `GetTitleIsActive`
6. Add survivors via `AddGameToListIfAcceptable`

### Admission rules

`AddGameToListIfAcceptable` rejects titles when:

- The path is a duplicate
- `KioskMeta.xml` is missing (unless fake metadata creation is enabled)
- A metadata wrapper exists but the linked retail title is not installed
- Game filter settings exclude retail or demo entries
- Full-game mode rewrites IDs via `MakeFullGameTitleID`

Runtime log strings include: `Title %016llX rejected for lack of KioskMeta.xml`.

### Special title IDs (hard-coded)

`ProcessSpecialTitleID` routes these explicitly:

| Title ID | Handling |
|----------|----------|
| `000500001FA82200` | Featured list |
| `000500001FA82300` | New releases |
| `000500001FA82400` | Active list / SES |
| `000500001FA82000` | About Wii U movie list |
| `000500001FA82100` | Attract mode movie list |
| `000500001FA83300` | About Amiibo movie list |

### KioskMeta.xml — the per-demo product sheet

Each kiosk-visible demo under `00050002` typically ships:

```text
meta/
  meta.xml              ← generic Wii U title metadata ("Non Playable Demo", etc.)
  KioskMeta.xml         ← kiosk-facing catalog card
  KioskMovie.mp4        ← optional trailer (plain MP4)
  KioskBoxArt_*.gtx     ← rating/region-specific box art
```

`KioskMeta.xml` carries what the menu needs to render a store tile:

- Region, product code, title ID, release date, genre code
- Player counts and controller lists
- Rating-board entries
- Flags: `demoFlg`, `movieFlg`, `movieIncludesRating`, `hasSpecialBox`, `rotatedBox`
- Localized blocks: `demoTitle`, `demoPublisher`, `genreDisp`, `tagLine`, `description`

Example flag combination for a **movie-only** wrapper: `demoFlg = 0`, `movieFlg = 1`. That matches the non-interactive / video-only code paths in MenuApp.

`KioskMovie.mp4` is a normal MP4 at a fixed path — replacing it with another encoded MP4 works; the menu plays whatever file is there.

There is also an `InstallMeta.xml` concept referenced at runtime for install-related flows.

---

## Featured, New, and Active lists

### Local XML (what homebrew replaces)

Featured and New lists live in separate installed titles:

- `meta/Featured.xml` — `<title_list type="featured">`
- `meta/NewReleases.xml` — `<title_list type="new release">`

Each `<title>` entry uses a full 16-hex demo ID, with `order`, `start_date`, and `end_date`. Runtime strings reject entries outside their date window.

MenuApp also references `DefaultFeaturedList.xml` as a possible fallback name.

### SES request format

`SESClass` builds explicit XML requests:

| Function | Request body | Channel tag |
|----------|--------------|-------------|
| `RequestFeaturedList` | `<request sequence="%d">featured</request>` | `title_list:featured` |
| `RequestNewReleaseList` | `<request sequence="%d">new releases</request>` | `title_list:new releases` |
| `RequestActiveList` | `<request sequence="%d">active</request>` | `title_list:active` |

Retail kiosks could refresh these lists remotely. Local XML on MLC is the other half — and what this repo targets.

### Active list fallback chain

Runtime strings describe a layered Active-list loader:

1. Try a save-data copy
2. If that fails, look for installed Active-list wrapper (`1fa82400`)
3. Parse `Active.xml` and apply date filtering

Status strings include `Successfully read Active list from save data copy` and `Featured title %016llX rejected because start date …`.

The menu keeps counts: `All Titles: %d, Featured: %d, New Releases: %d`.

---

## Movies and attract mode

### File discovery in `MenuConfigurationClass`

Movie lists are built by scanning a title's `meta/` directory — not from a hidden compiled table.

**About Wii U** — looks for `AboutWiiU%02d.mp4` (six slots). It may also look for optional `AboutWiiU%02d.gtx` textures and run `CheckForAlternateAboutWiiUButtons` — custom per-video button art. Retail About Wii U titles usually ship **MP4s only**; the on-screen labels come from Kiosk Menu's `MessageStudio.xml`, so missing `.gtx` is normal.

**About Amiibo** — same for `AboutAmiibo%02d.mp4`. Optional alternate buttons may use names like `AboutAmiibo%02dButtonDown.gtx` / `ButtonUp.gtx` (pressed vs unpressed). Also absent on typical installs.

**`.gtx` elsewhere that *is* used:** demo wrappers under `00050002` often include `KioskBoxArt_*.gtx` for carousel box art — unrelated to About Wii U button overrides.

**Attract mode** — scans `meta/` for filenames beginning with `AttractMode`, parses a two-digit index from the name (e.g. `AttractMode07.mp4`), and builds a rotating playlist. Decompiled code allocates an internal table with **room for up to 100 slots** — that is a code limit, not a retail content count. Known kiosk installs use **12 clips**: `AttractMode00.mp4` … `AttractMode11.mp4` (see [AttractMode.MD](Title/AttractMode.MD)). `GetNextAttractModeMovie` walks whatever files were found and wraps around.

### In-menu playback vs helper titles

Two playback paths coexist:

1. **Inside MenuApp** — `MenuScreenAboutWiiUClass::PlaySelectedMovie` and similar fetch a path from `MenuConfigurationClass`, set `MenuScreenMoviePlayerClass`, and play through `MoviePlayerClass` (backed by `mvplayer.rpl`).
2. **Separate helper titles** — About Wii U / Attract / About Amiibo can also be launched as installed titles; MenuApp may pass a clip index when exiting the menu.

`MenuScreenGameSelectorClass::PlayMovie` uses `GetGameLibraryClass::GetMovieFile()` for carousel video, or `GetNextAttractModeMovie()` when in attract mode. Output mode depends on `GetAttractModeMode()`.

### Attract mode behavior

Attract mode is first-class, not just an idle timeout:

- Explicit configuration state (`attractModeMode`)
- Playlist rotation from `AttractMode00.mp4` … `AttractMode11.mp4` in the attract title's `meta/` (12 clips on known retail installs; MenuApp's internal table can hold more if present)
- Language-specific kiosk movies: `KioskMovie_US_ENGLISH.mp4`, `KioskMovie_JP_JAPANESE.mp4`, etc.
- Maintenance UI to set attract mode mode
- Invalid-value fallback: `SetAttractModeMode(): invalid value (%d)--defaulting to ATTRACT_MODE_MODE_NORMAL`

### Non-interactive mode

Separate subsystem: `MenuScreenNonInteractiveModeClass`, `GetNonInteractiveMovieList()`, `ProcessNonInteractiveMovieList()`. May enumerate movies through MCP title list rather than fixed filenames only.

Generic path string also seen: `/meta/KioskMovie.mp4`.

---

## Launching games and demos

### Deferred launch via `MenuScreenLaunchGameClass`

The selector does not jump directly to a game. Launch intent is stored, then consumed during orderly shutdown:

- `SetTitleIDToLaunch` — explicit override
- Otherwise `GetLaunchedGameTitleID` reads the selected index from `GameLibraryClass`
- `GetLaunchedGameTitlePath` returns a demo path only when there is no override, a valid selection exists, and the library ID matches the demo ID

### Three launch modes in `LaunchTitle`

`CafeMenuPatchClass::LaunchTitle`:

1. System updater (with `kiosk` argument/tag)
2. Launch by filesystem path
3. Launch by title ID

Before launch, inactivity reset timers may change: 120 seconds for standard units, 300 seconds for full-game units (when launching something other than the menu itself or the updater).

Cold-boot relaunch: menu can detect that state, log `Relaunching on cold boot`, push the menu title ID into the launch screen, and exit to relaunch itself.

### Rating and accessory gates

MessageStudio defines pre-launch prompts:

- Rating agreement (Yes/No) — Japan/CERO variants and ESRB T/M lines
- Accessory/controller compatibility overlay: `This demo supports the controllers shown below.`

Likely pipeline:

1. User taps Play Demo or Play Game
2. Menu checks rating/region rules
3. Optional rating confirmation
4. Optional accessory screen
5. Launch or return to selector on cancel

`MenuConfigurationClass` exposes setters/getters for rating-board and confirmation behavior.

### HOME / demo constraints

Strings around demo exit and HOME behavior imply the kiosk redirects or blocks normal system calls during demos (eShop, browser, eManual, etc.).

---

## SES and fleet management

Retail kiosks were designed for remote management, not static NAND-only operation.

### MenuApp side (`SESClass`)

Named functions include:

- `SendHeartbeat`, `Run`, `DoPCHostCommunication`, `DoBOSSCommunication`
- `RequestFeaturedList`, `RequestNewReleaseList`, `RequestActiveList`
- `RequestTime`, `ReportState`

MenuApp constructs high-level requests; `SESClient.rpl` handles protocol details.

### SESClient side (persistent state)

String and symbol evidence for XML state files:

- `sesclient.download_state.xml`
- `sesclient.ses_client_settings.xml`
- `sesclient.installed_titles.xml`
- `sesclient.pending.xml`
- `sesclient.poll_state.xml`

Endpoints seen in strings (historical retail infrastructure):

- `https://sess.nintendo.com:4343`
- `https://sesk.nintendo.com:4446/challenge.php`

Protocol vocabulary: heartbeat, title_list, CHECK_FOR_REQUESTS, REQUEST_SESSION_KEY, AUTHENTICATE_HOST, install_disk.

### Install reconciliation (retail fleet logic)

`ValidateInstalled` compares server-reported titles against persisted `InstalledTitles` XML and categorizes:

- newly installed
- installed missed
- unknown installed
- dead orphans (removed)

`InstallReady` gates installs on date/time windows and client settings (`use_install_window`).

`InstallActivator` may queue reboot when: new disk ready, delete pending, pending firmware update — but only inside allowed maintenance windows.

`DeleteTitle` is a multi-step orchestrated workflow, not a single delete call.

**Note for homebrew users:** none of this is required to run replacement Featured/New/About titles on a home console. It explains why retail units behaved the way they did.

---

## Media playback (`mvplayer.rpl`)

`MoviePlayerClass` in MenuApp wraps this library.

### Capabilities

Imports and symbols point to:

- H.264 decode (`H264DEC*`)
- AAC audio (`AACDEC*`, `AudioPlayer`, `snd_core`)
- GX2 rendering, separate TV and DRC draw paths
- libcurl / HTTP / HLS (`HTTPLiveSource`, `m3u8`)

MIME/extension handling for MP4, MOV, MPEG-TS, AVI, WebM, WMV, AAC, MP3, and others.

Key string: `Run media stream, eg: http://a.com/video.m3u8, /vol/external01/a.mp4` — one stack handles both URLs and local paths.

Filesystem imports (`FSOpenFile`, `FSReadFile`, …) confirm local file playback.

Caveat from strings: `File above 4 GB - supported only through HTTP but not from local file system`.

### Split of responsibility

| Component | Role |
|-----------|------|
| MenuApp | Choose source path, screen state, TV/DRC mode |
| mvplayer.rpl | Detect source type, decode, buffer, render, seek/pause |

Exported API surface includes `Create`, `Destroy`, `CanPlayType`, `GetTypeFromExtension`, and observer callbacks for state/buffering/frame updates.

---

## Confidence levels

### High confidence

- `1fa81000` / `MenuApp.rpx` is the kiosk menu shell
- `mvplayer.rpl` and `SESClient.rpl` are required companions
- Region defaults come from `DefaultMenuConfiguration*.xml`
- `MessageStudio.xml` is the central UI string table
- Named screen classes exist for selector, categories, About Wii U/Amiibo, movie player, launch
- Featured / New / Active list code paths and XML shapes are real
- About Wii U is a six-button video chooser
- In-menu movie playback uses `MoviePlayerClass` + `mvplayer.rpl`
- Demo admission requires `KioskMeta.xml` in normal mode
- Launch flow includes rating and accessory prompts
- Special helper title IDs are hard-coded in `ProcessSpecialTitleID`

### Medium confidence

- Featured/New rows are populated from installed list titles plus optional SES refresh
- About/Attract/Amiibo helper titles are sometimes launched by title ID with clip index
- Active list uses save-data → installed-wrapper fallback
- Some playback happens in-menu; some delegates to helper titles depending on screen/mode

### Low confidence / still open

- Exact in-memory structures for the game library
- Exact genre-to-title mapping source (compiled vs derived)
- Precise attract-mode timeout triggers
- Full division of labor between `SESClass` and `SESClient.rpl` for featured/new request fulfillment (MenuRequestResponder logs some types as "not supported here")
- Complete non-interactive mode title enumeration rules

---

## Still unknown

Worth deeper RE if someone continues Ghidra work on retail binaries:

1. Full carousel population logic and in-memory title metadata layout
2. Exact featured/new remote-vs-local fallback interaction on disconnected home setups
3. Complete `mvplayer.rpl` ↔ `MoviePlayerClass` binding
4. Any companion database file beyond `KioskMeta.xml` / list XML not yet located
5. Runtime title IDs launched for each About Wii U button in all configurations

Good next targets: more of `MenuApp.rpx`, plus full passes on `mvplayer.rpl` and `SESClient.rpl` (already started — summaries above).

---

## Methodology

Analysis pipeline used for this document:

1. Extract the retail `1fa81000` title from a kiosk MLC dump
2. Load `MenuApp.rpx`, `mvplayer.rpl`, and `SESClient.rpl` in Ghidra (RPX loader)
3. Decompile key functions (`main`, `LaunchTitle`, movie-list builders, SES request builders, install reconcilers)
4. Cross-check string tables against `MessageStudio.xml` and runtime memory strings
5. Validate `KioskMeta.xml` / `KioskMovie.mp4` behavior against sampled `00050002` wrapper titles

Tools credited in the [project README](../README.md): Ghidra, GhidraRPXLoader, Cursor AI for structuring notes, helping decompile, and cross-referencing findings.
