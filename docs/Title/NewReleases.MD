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

FTP-ready tree after build: [`Release/1fa82300/`](../../Release/1fa82300/).

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

Build the ID from the `00050002` folder:

```text
00050002 + 10128500  ->  0005000210128500
```

Like Featured, kiosk menu often cares about the **stub** / tile ID (`...FF`) rather than the playable sibling. Use the ID that matches how your kiosk menu presents the title.

If unsure you can add both.

Example:

```xml
<title order="2" start_date="2012-01-01 00:00:00" end_date="2035-01-01 23:59:59">00050002101CE4FF</title>
```

---

## Add or remove demos

1. Install the demo under `mlc/usr/title/00050002/`.
2. Edit `Release/1fa82300/meta/NewReleases.xml` (the generator will not overwrite it).
3. Add or remove `<title ...>` lines.
4. Upload the changed file or full title.
5. Reboot or re-open Kiosk Menu.

Removing a line only removes it from the **New** row. It can still appear under **All Titles** or **Featured** if those sources still reference it.

---

## Install

1. Build the project: [HowToBuild.MD](../HowToBuild.MD#new-releases--1fa82300).
2. Upload [`Release/1fa82300/`](../../Release/1fa82300/) to `mlc:/usr/title/00050000/1fa82300/`.
3. Reboot and test in Kiosk Menu.

Per-folder install layout: [Release/README.md](../../Release/README.md).

---

## Troubleshooting

| Issue | Check |
|-------|-------|
| New row is empty | `NewReleases.xml` missing, broken, or all dates are out of range |
| Title listed but not visible | Wrong `00050002` ID, wrong region, or demo not installed |
| Wrong order | Duplicate / out-of-order `order` values |
| Wrong demo in New row | Wrong `00050002` ID in `NewReleases.xml`, or duplicate / conflicting `order` values |
| `???` on Wii U Menu | Normal for helper titles |

Related:

- [FeaturedList.MD](FeaturedList.MD)
- [HowKioskMenuWorks.MD](../HowKioskMenuWorks.MD)
