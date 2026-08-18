# Featured List (`1fa82200`)

Controls which kiosk demos appear under **Featured** in Kiosk Menu.

- **Title ID:** `000500001FA82200`
- **MLC path:** `mlc/usr/title/00050000/1fa82200/`
- **RPX:** `title_list.rpx`
- **List file:** `meta/Featured.xml`

Kiosk Menu reads `Featured.xml` from this title's `meta/` folder.

---

## Folder layout

```text
1fa82200/
  code/
    title_list.rpx
    app.xml
    cos.xml
  meta/
    Featured.xml
    meta.xml
```

Pre-built in releases: `1fa82200/` inside [All-In-One](../../Release/All-In-One/).

---

## `Featured.xml` format

```xml
<?xml version="1.0" encoding="utf-8"?>
<title_list type="featured">
	<title order="1" start_date="2000-01-01 01:01:01" end_date="2038-12-31 23:59:59">000500021FA82201</title>
</title_list>
```

| Field | Meaning |
|------|---------|
| `order` | Sort order, lower numbers first |
| `start_date` / `end_date` | Date + time when the entry is active |
| element body | Full **16-hex** demo title ID |

The sample ID `000500021FA82201` is a **placeholder**. Replace it with a real demo title you have installed.

---

## Which title ID to use

Demo tiles live under `mlc/usr/title/00050002/<8-char-id>/`.

```text
00050002 + 10128500  ->  0005000210128500
```

For kiosk menu tiles, the **stub** (`...FF`) is often the right ID — use the ID your kiosk menu actually expects.

Example:

```xml
<title order="2" start_date="2012-01-01 00:00:00" end_date="2035-01-01 23:59:59">00050002101DB4FF</title>
```

---

## Customize

1. Make sure each demo is installed under `mlc/usr/title/00050002/`.
2. Edit `meta/Featured.xml` — add or remove `<title ...>` lines.
3. Re-upload the file or full title, then reboot or re-open Kiosk Menu.

Removing a line hides that title from **Featured** only; it can still appear elsewhere.

---

## Install

1. Download the latest release from [GitHub Releases](https://github.com/pumpk-bit/Wii-U-Kiosk-Homebrew/releases). Use the `1fa82200/` folder from **All-In-One**.
2. Edit `meta/Featured.xml` with your demo title IDs.
3. FTP the folder to `mlc:/usr/title/00050000/1fa82200/`.
4. Reboot and open Kiosk Menu.

To compile yourself: [HowToBuild.MD](../HowToBuild.MD). File checklist: [Release/README.md](../../Release/README.md).

---

## Troubleshooting

| Issue | Check |
|-------|-------|
| Featured row is empty | `Featured.xml` missing, broken, or all dates are out of range |
| Title listed but not visible | Wrong `00050002` ID, wrong region, or demo not installed |
| Wrong order | Duplicate / out-of-order `order` values |
| Wrong demo in Featured row | Wrong ID in `Featured.xml`, or conflicting `order` values |
| `???` on Wii U Menu | Normal for helper titles |

Related:

- [NewReleases.MD](NewReleases.MD)
- [HowKioskMenuWorks.MD](../HowKioskMenuWorks.MD)
