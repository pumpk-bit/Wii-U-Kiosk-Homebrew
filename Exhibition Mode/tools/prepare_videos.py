#!/usr/bin/env python3
"""Copy user videos into Exhibition Mode meta/ as TVnn.mp4 + DRCnn.mp4 pairs.

MenuApp requires the same number of TV and DRC clips and exact names:

  TV00.mp4 .. TV99.mp4   (8 characters)
  DRC00.mp4 .. DRC99.mp4 (9 characters)

Examples:

  python tools/prepare_videos.py \\
    --tv tv_clip1.mp4 tv_clip2.mp4 \\
    --drc pad_clip1.mp4 pad_clip2.mp4 \\
    --out ../../Release/1fa82700/meta

  python tools/prepare_videos.py \\
    --pairs lobby_tv.mp4:lobby_pad.mp4 intro_tv.mp4:intro_pad.mp4 \\
    --out ../../Release/1fa82700/meta
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


def copy_pair(index: int, tv_src: Path, drc_src: Path, out_dir: Path, link: bool) -> None:
    if not tv_src.is_file():
        raise SystemExit(f"TV source not found: {tv_src}")
    if not drc_src.is_file():
        raise SystemExit(f"DRC source not found: {drc_src}")
    if index < 0 or index > 99:
        raise SystemExit(f"Slot index out of range (0-99): {index}")

    out_dir.mkdir(parents=True, exist_ok=True)
    tv_dst = out_dir / f"TV{index:02d}.mp4"
    drc_dst = out_dir / f"DRC{index:02d}.mp4"

    for src, dst in ((tv_src, tv_dst), (drc_src, drc_dst)):
        if link:
            if dst.exists():
                dst.unlink()
            dst.symlink_to(src.resolve())
        else:
            shutil.copy2(src, dst)
        print(f"  {src.name} -> {dst.name}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--out", type=Path, required=True, help="Destination meta/ folder")
    p.add_argument("--tv", nargs="+", type=Path, help="TV clips in playlist order")
    p.add_argument("--drc", nargs="+", type=Path, help="GamePad clips in playlist order")
    p.add_argument(
        "--pairs",
        nargs="+",
        metavar="TV:DRC",
        help="Colon-separated TV:DRC paths, one pair per slot",
    )
    p.add_argument(
        "--link",
        action="store_true",
        help="Symlink instead of copy (saves space while testing locally)",
    )
    p.add_argument(
        "--start",
        type=int,
        default=0,
        help="First slot index (default 0)",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    pairs: list[tuple[Path, Path]] = []

    if args.pairs:
        for item in args.pairs:
            if ":" not in item:
                raise SystemExit(f"Expected TV:DRC pair, got {item!r}")
            tv_s, drc_s = item.split(":", 1)
            pairs.append((Path(tv_s), Path(drc_s)))
    elif args.tv and args.drc:
        if len(args.tv) != len(args.drc):
            raise SystemExit(f"TV count ({len(args.tv)}) != DRC count ({len(args.drc)})")
        pairs = list(zip(args.tv, args.drc))
    else:
        raise SystemExit("Provide --pairs TV:DRC ... or both --tv and --drc")

    print(f"Writing {len(pairs)} pair(s) to {args.out.resolve()}")
    for i, (tv, drc) in enumerate(pairs):
        copy_pair(args.start + i, tv, drc, args.out, args.link)
    print("Done. Enable Exhibition Mode in Kiosk Menu maintenance settings.")


if __name__ == "__main__":
    main()
