#!/usr/bin/env python3
"""Decompress Wii U RPX/RPL sections and dump strings.

Usage:
    python tools/unpack_rpx.py <input.rpx> [output_dir]
"""
from __future__ import annotations

import struct
import sys
import zlib
from pathlib import Path

SHF_RPL_COMPRESSED = 0x08000000
SHT_NOBITS = 8


def read_elf(data: bytes) -> tuple[list[dict], bytes]:
    if data[:4] != b"\x7fELF":
        raise ValueError("not ELF")
    ei_class = data[4]
    ei_data = data[5]
    endian = ">" if ei_data == 2 else "<"
    if ei_class != 1:
        raise ValueError("expected ELF32")
    e_shoff, e_shentsize, e_shnum, e_shstrndx = struct.unpack_from(
        endian + "IHHHH", data, 32
    )[0], *struct.unpack_from(endian + "HHHH", data, 40)[1:]
    # e_shoff at 32, then e_flags(4) e_ehsize(2) e_phentsize(2) e_phnum(2) e_shentsize(2) e_shnum(2) e_shstrndx(2)
    e_shoff = struct.unpack_from(endian + "I", data, 32)[0]
    e_shentsize, e_shnum, e_shstrndx = struct.unpack_from(endian + "HHH", data, 46)
    sections = []
    for i in range(e_shnum):
        off = e_shoff + i * e_shentsize
        sh_name, sh_type, sh_flags, sh_addr, sh_offset, sh_size, sh_link, sh_info, sh_addralign, sh_entsize = struct.unpack_from(
            endian + "IIIIIIIIII", data, off
        )
        sections.append(
            {
                "name_off": sh_name,
                "type": sh_type,
                "flags": sh_flags,
                "addr": sh_addr,
                "offset": sh_offset,
                "size": sh_size,
                "index": i,
            }
        )
    strtab = sections[e_shstrndx]
    raw = data[strtab["offset"] : strtab["offset"] + strtab["size"]]
    # shstrtab itself may be compressed
    if strtab["flags"] & SHF_RPL_COMPRESSED and strtab["type"] != SHT_NOBITS:
        raw = zlib.decompress(data[strtab["offset"] + 4 : strtab["offset"] + strtab["size"]])
    for s in sections:
        end = raw.find(b"\x00", s["name_off"])
        s["name"] = raw[s["name_off"] : end].decode("ascii", "replace")
    return sections, data


def section_bytes(data: bytes, s: dict) -> bytes:
    if s["type"] == SHT_NOBITS or s["size"] == 0:
        return b""
    blob = data[s["offset"] : s["offset"] + s["size"]]
    if s["flags"] & SHF_RPL_COMPRESSED:
        uncomp_size = struct.unpack(">I", blob[:4])[0]
        out = zlib.decompress(blob[4:])
        if len(out) != uncomp_size:
            # some tools store size as the compressed payload length; still usable
            pass
        return out
    return blob


def extract_strings(blob: bytes, min_len: int = 5) -> list[str]:
    out: list[str] = []
    buf = bytearray()
    for b in blob:
        if 32 <= b <= 126:
            buf.append(b)
        else:
            if len(buf) >= min_len:
                out.append(buf.decode("ascii"))
            buf.clear()
    if len(buf) >= min_len:
        out.append(buf.decode("ascii"))
    return out


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("Usage: python tools/unpack_rpx.py <input.rpx> [output_dir]", file=sys.stderr)
        sys.exit(0 if len(sys.argv) > 1 else 2)
    path = Path(sys.argv[1])
    if not path.is_file():
        raise SystemExit(f"not a file: {path}")
    data = path.read_bytes()
    sections, data = read_elf(data)
    dump_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else path.with_suffix("")
    dump_dir.mkdir(parents=True, exist_ok=True)
    all_strings: list[str] = []
    print("idx  name                     addr     size     flags    compressed")
    for s in sections:
        payload = section_bytes(data, s)
        comp = bool(s["flags"] & SHF_RPL_COMPRESSED)
        print(
            f"{s['index']:3d}  {s['name']:<24} {s['addr']:08X} {len(payload):8d} {s['flags']:08X} {comp}"
        )
        if payload and s["name"] not in ("", ".rela.text", ".rela.rodata", ".rela.data"):
            (dump_dir / f"{s['index']:02d}{s['name'].replace('.', '_') or '_null'}").write_bytes(payload)
            if s["name"] in (".rodata", ".data", ".strtab", ".text"):
                all_strings.extend(extract_strings(payload))
    strings_path = dump_dir / "strings.txt"
    uniq = []
    seen = set()
    for s in all_strings:
        if s not in seen:
            seen.add(s)
            uniq.append(s)
    strings_path.write_text("\n".join(uniq), encoding="utf-8")
    print(f"\nWrote {len(uniq)} strings to {strings_path}")


if __name__ == "__main__":
    main()
