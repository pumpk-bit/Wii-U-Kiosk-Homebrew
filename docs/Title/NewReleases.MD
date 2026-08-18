# New Releases (`1fa82300`)

Controls which kiosk demos appear under **New** in Kiosk Menu.

- **Title ID:** `000500001FA82300`
- **MLC path:** `mlc/usr/title/00050000/1fa82300/`
- **RPX:** `newreleases_wrapper.rpx`
- **List file:** `meta/NewReleases.xml`

Same idea as Featured List, but with a different file name and XML type.

---

## Folder layout

```text
1fa82300/
  code/
    newreleases_wrapper.rpx
    app.xml
    cos.xml
  meta/
    NewReleases.xml
    meta.xml
```

---

## `NewReleases.xml` format

```xml
<?xml version="1.0" encoding="utf-8"?>
<title_list type="new release">
	<title order="1" start_date="2000-01-01 01:01:01" end_date="2038-12-31 23:59:59">000500021FA82301</title>
</title_list>
```

| Field | Meaning |
|------|---------|
| `order` | Sort order in the New row |
| `start_date` / `end_date` | Active date range |
| element body | Full **`00050002`** demo title ID |

The sample ID `000500021FA82301` is fictional. Replace it with a real demo you installed.

---

## Which title ID to use

```text
00050002 + 10128500  ->  0005000210128500
```

Like Featured, kiosk menu often cares about the **stub** / tile ID (`...FF`). Use the ID that matches how your kiosk menu presents the title.

Example:

```xml
<title order="2" start_date="2012-01-01 00:00:00" end_date="2035-01-01 23:59:59">00050002101CE4FF</title>
```

---

## Customize

1. Install each demo under `mlc/usr/title/00050002/`.
2. Edit `meta/NewReleases.xml`, add or remove `<title ...>` lines.
3. Re-upload the file or full title, then reboot or re-open Kiosk Menu.

Removing a line only removes it from the **New** row.

---

## Install

1. Download the latest release from [GitHub Releases](https://github.com/pumpk-bit/Wii-U-Kiosk-Homebrew/releases). Use the `1fa82300/` folder from **All-In-One**.
2. Edit `meta/NewReleases.xml` with your demo title IDs.
3. FTP the folder to `mlc:/usr/title/00050000/1fa82300/`.
4. Reboot and open Kiosk Menu.

To compile yourself: [HowToBuild.MD](../HowToBuild.MD). 

---

## Troubleshooting

| Issue | Check |
|-------|-------|
| New row is empty | `NewReleases.xml` missing, broken, or all dates are out of range |
| Title listed but not visible | Wrong `00050002` ID, wrong region, or demo not installed |
| Wrong order | Duplicate / out-of-order `order` values |
| Wrong demo in New row | Wrong ID in `NewReleases.xml`, or conflicting `order` values |
| `???` on Wii U Menu | Normal for helper titles |

Related:

- [FeaturedList.MD](FeaturedList.MD)
- [HowKioskMenuWorks.MD](../HowKioskMenuWorks.MD)
