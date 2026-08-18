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

FTP-ready tree: [`Release/1fa82200/`](../../Release/1fa82200/).

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

The sample ID `000500021FA82201` in this repo is a **placeholder**. Replace it with a real demo title you have installed.

---

## Which title ID to use

Demo tiles live under:

`mlc/usr/title/00050002/<8-char-id>/`

Build the full title like this:

```text
00050002 + 10128500  ->  0005000210128500
```

For kiosk menu tiles, the **stub** (`...FF`) is often the right ID to use because that is what the carousel shows. Use the title ID your kiosk menu actually expects for that entry.

Example:

```xml
<title order="2" start_date="2012-01-01 00:00:00" end_date="2035-01-01 23:59:59">00050002101DB4FF</title>
```

---

## Add or remove demos

1. Make sure the demo is installed under `mlc/usr/title/00050002/`.
2. Edit `meta/Featured.xml`.
3. Add or remove `<title ...>` lines.
4. Upload the changed file or full title.
5. Reboot or re-open Kiosk Menu.

Remove a line to hide that title from **Featured**. The demo can still exist on NAND and still appear elsewhere.

---

## Install

1. Build the project: [HowToBuild.MD](../HowToBuild.MD#featured-list--1fa82200).
2. Upload [`Release/1fa82200/`](../../Release/1fa82200/) to `mlc:/usr/title/00050000/1fa82200/`.
3. Reboot and open Kiosk Menu.

Per-folder install layout: [Release/README.md](../../Release/README.md).

---

## Troubleshooting

| Issue | Check |
|-------|-------|
| Featured row is empty | `Featured.xml` missing, broken, or all dates are out of range |
| Title listed but not visible | Wrong `00050002` ID, wrong region, or demo not installed |
| Wrong order | Duplicate / out-of-order `order` values |
| No demo | Check the order. Make sure there are no duplicates. |
| `???` on Wii U Menu | Normal for helper titles |

Related:

- [NewReleases.MD](NewReleases.MD)
- [HowKioskMenuWorks.MD](../HowKioskMenuWorks.MD)
