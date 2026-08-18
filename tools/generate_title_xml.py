#!/usr/bin/env python3
"""Generate Cafe title XML into Release/<unique-id>/.

Run from anywhere:

    python tools/generate_title_xml.py
    python tools/generate_title_xml.py featured
    python tools/generate_title_xml.py --project "Featured List"

Catalog lists (Featured.xml / NewReleases.xml) are written once. Later runs
keep whatever titles you edited in Release/.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

if sys.version_info < (3, 8):
    sys.exit("Python 3.8 or newer is required to generate title XML.")

REPO = Path(__file__).resolve().parent.parent

OS_VERSION = "000500101000400a"
GROUP_ID = "00010000"
PUBLISHER = "Homebrew"
MASTERING_DATE = "2026-08-18 00.00.00"

TITLES: dict[str, dict[str, Any]] = {
    "featured": {
        "dir": "Featured List",
        "unique": "1fa82200",
        "tid": "000500001FA82200",
        "rpx": "title_list.rpx",
        "long_name": "Featured List",
        "short_name": "Featured",
        "product_code": "WUP-P-HBFL",
        "sdk_version": "20703",
        "list": {
            "filename": "Featured.xml",
            "type": "featured",
            "placeholder": "000500021FA82201",
        },
    },
    "newreleases": {
        "dir": "New Releases",
        "unique": "1fa82300",
        "tid": "000500001FA82300",
        "rpx": "newreleases_wrapper.rpx",
        "long_name": "New Releases",
        "short_name": "New",
        "product_code": "WUP-P-HBNR",
        "sdk_version": "20703",
        "list": {
            "filename": "NewReleases.xml",
            "type": "new release",
            "placeholder": "000500021FA82301",
        },
    },
    "aboutwiiu": {
        "dir": "About Wii U",
        "unique": "1fa82000",
        "tid": "000500001FA82000",
        "rpx": "aboutwiiu_wrapper.rpx",
        "long_name": "About Wii U",
        "short_name": "About",
        "product_code": "WUP-P-HBAU",
        "sdk_version": "20701",
    },
    "attractmode": {
        "dir": "Attract Mode",
        "unique": "1fa82100",
        "tid": "000500001FA82100",
        "rpx": "attractmode_wrapper.rpx",
        "long_name": "Attract Mode",
        "short_name": "Attract",
        "product_code": "WUP-P-HBAM",
        "sdk_version": "20701",
    },
    "aboutamiibo": {
        "dir": "About Amiibo",
        "unique": "1fa83300",
        "tid": "000500001FA83300",
        "rpx": "aboutamiibo_wrapper.rpx",
        "long_name": "About Amiibo",
        "short_name": "Amiibo",
        "product_code": "WUP-P-HBAA",
        "sdk_version": "20701",
    },
}

DIR_TO_SLUG = {spec["dir"]: slug for slug, spec in TITLES.items()}
UNIQUE_TO_SLUG = {spec["unique"]: slug for slug, spec in TITLES.items()}


def app_xml(title_id: str, sdk_version: str) -> str:
    return f"""<?xml version="1.0" encoding="utf-8"?>
<app type="complex" access="777">
  <version type="unsignedInt" length="4">14</version>
  <os_version type="hexBinary" length="8">{OS_VERSION}</os_version>
  <title_id type="hexBinary" length="8">{title_id}</title_id>
  <title_version type="hexBinary" length="2">0000</title_version>
  <sdk_version type="unsignedInt" length="4">{sdk_version}</sdk_version>
  <app_type type="hexBinary" length="4">80000000</app_type>
  <group_id type="hexBinary" length="4">{GROUP_ID}</group_id>
</app>
"""


def cos_xml(rpx_name: str) -> str:
    return f"""<?xml version="1.0" encoding="utf-8"?>
<app type="complex" access="777">
  <version type="unsignedInt" length="4">16</version>
  <cmdFlags type="unsignedInt" length="4">0</cmdFlags>
  <argstr type="string" length="4096">{rpx_name}</argstr>
  <avail_size type="hexBinary" length="4">00000000</avail_size>
  <codegen_size type="hexBinary" length="4">00000000</codegen_size>
  <codegen_core type="hexBinary" length="4">00000001</codegen_core>
  <max_size type="hexBinary" length="4">80000000</max_size>
  <max_codesize type="hexBinary" length="4">0e000000</max_codesize>
  <permissions type="complex">
    <p0 type="complex"><group type="unsignedInt" length="4"> 1</group><mask type="hexBinary" length="8">000000000000FF00</mask></p0>
    <p1 type="complex"><group type="unsignedInt" length="4"> 3</group><mask type="hexBinary" length="8">0000000000000007</mask></p1>
    <p2 type="complex"><group type="unsignedInt" length="4"> 9</group><mask type="hexBinary" length="8">FFFFFFFFFFFFFFFF</mask></p2>
    <p3 type="complex"><group type="unsignedInt" length="4">12</group><mask type="hexBinary" length="8">0000000000000001</mask></p3>
    <p4 type="complex"><group type="unsignedInt" length="4">11</group><mask type="hexBinary" length="8">FFFFFFFFFFFFFFFF</mask></p4>
    <p5 type="complex"><group type="unsignedInt" length="4">13</group><mask type="hexBinary" length="8">00000000000000FF</mask></p5>
    <p6 type="complex"><group type="unsignedInt" length="4">14</group><mask type="hexBinary" length="8">0000000000000000</mask></p6>
    <p7 type="complex"><group type="unsignedInt" length="4">15</group><mask type="hexBinary" length="8">0000000000000003</mask></p7>
    <p8 type="complex"><group type="unsignedInt" length="4">16</group><mask type="hexBinary" length="8">0000000000000003</mask></p8>
    <p9 type="complex"><group type="unsignedInt" length="4">17</group><mask type="hexBinary" length="8">0000000000000001</mask></p9>
    <p10 type="complex"><group type="unsignedInt" length="4">18</group><mask type="hexBinary" length="8">0000000000000001</mask></p10>
    <p11 type="complex"><group type="unsignedInt" length="4">19</group><mask type="hexBinary" length="8">0000000000000001</mask></p11>
    <p12 type="complex"><group type="unsignedInt" length="4">20</group><mask type="hexBinary" length="8">0000000000000003</mask></p12>
    <p13 type="complex"><group type="unsignedInt" length="4">21</group><mask type="hexBinary" length="8">0000000000000001</mask></p13>
    <p14 type="complex"><group type="unsignedInt" length="4">22</group><mask type="hexBinary" length="8">0000000000000001</mask></p14>
  </permissions>
  <default_stack0_size type="hexBinary" length="4">00000000</default_stack0_size>
  <default_stack1_size type="hexBinary" length="4">00000000</default_stack1_size>
  <default_stack2_size type="hexBinary" length="4">00000000</default_stack2_size>
  <default_redzone0_size type="hexBinary" length="4">00000000</default_redzone0_size>
  <default_redzone1_size type="hexBinary" length="4">00000000</default_redzone1_size>
  <default_redzone2_size type="hexBinary" length="4">00000000</default_redzone2_size>
  <exception_stack0_size type="hexBinary" length="4">00001000</exception_stack0_size>
  <exception_stack1_size type="hexBinary" length="4">00001000</exception_stack1_size>
  <exception_stack2_size type="hexBinary" length="4">00001000</exception_stack2_size>
</app>
"""


def meta_xml(
    title_id: str,
    long_name: str,
    short_name: str,
    publisher: str,
    product_code: str,
) -> str:
    locales = (
        "ja",
        "en",
        "fr",
        "de",
        "it",
        "es",
        "zhs",
        "ko",
        "nl",
        "pt",
        "ru",
        "zht",
    )

    def names(tag: str, value: str, length: int) -> str:
        return "\n".join(
            f'  <{tag}_{loc} type="string" length="{length}">{value}</{tag}_{loc}>'
            for loc in locales
        )

    addons = "\n".join(
        f'  <add_on_unique_id{i} type="hexBinary" length="4">00000000</add_on_unique_id{i}>'
        for i in range(32)
    )
    return f"""<?xml version="1.0" encoding="utf-8"?>
<menu type="complex" access="777">
  <version type="unsignedInt" length="4">32</version>
  <product_code type="string" length="32">{product_code}</product_code>
  <content_platform type="string" length="32">WUP</content_platform>
  <company_code type="string" length="8">0000</company_code>
  <mastering_date type="string" length="32">{MASTERING_DATE}</mastering_date>
  <logo_type type="unsignedInt" length="4">0</logo_type>
  <app_launch_type type="hexBinary" length="4">00000000</app_launch_type>
  <invisible_flag type="hexBinary" length="4">00000000</invisible_flag>
  <no_managed_flag type="hexBinary" length="4">00000000</no_managed_flag>
  <no_event_log type="hexBinary" length="4">00000000</no_event_log>
  <no_icon_database type="hexBinary" length="4">00000000</no_icon_database>
  <launching_flag type="hexBinary" length="4">00000000</launching_flag>
  <install_flag type="hexBinary" length="4">00000000</install_flag>
  <closing_msg type="unsignedInt" length="4">0</closing_msg>
  <title_version type="unsignedInt" length="4">0</title_version>
  <title_id type="hexBinary" length="8">{title_id}</title_id>
  <group_id type="hexBinary" length="4">{GROUP_ID}</group_id>
  <boss_id type="hexBinary" length="8">0000000000000000</boss_id>
  <os_version type="hexBinary" length="8">{OS_VERSION}</os_version>
  <app_size type="hexBinary" length="8">0000000000000000</app_size>
  <common_save_size type="hexBinary" length="8">0000000000400000</common_save_size>
  <account_save_size type="hexBinary" length="8">0000000000200000</account_save_size>
  <common_boss_size type="hexBinary" length="8">0000000000400000</common_boss_size>
  <account_boss_size type="hexBinary" length="8">0000000000100000</account_boss_size>
  <save_no_rollback type="unsignedInt" length="4">0</save_no_rollback>
  <join_game_id type="hexBinary" length="4">00000000</join_game_id>
  <join_game_mode_mask type="hexBinary" length="8">0000000000000000</join_game_mode_mask>
  <bg_daemon_enable type="unsignedInt" length="4">1</bg_daemon_enable>
  <olv_accesskey type="unsignedInt" length="4">0</olv_accesskey>
  <wood_tin type="unsignedInt" length="4">0</wood_tin>
  <e_manual type="unsignedInt" length="4">0</e_manual>
  <e_manual_version type="unsignedInt" length="4">0</e_manual_version>
  <region type="hexBinary" length="4">00000002</region>
  <pc_cero type="unsignedInt" length="4">0</pc_cero>
  <pc_esrb type="unsignedInt" length="4">0</pc_esrb>
  <pc_bbfc type="unsignedInt" length="4">192</pc_bbfc>
  <pc_usk type="unsignedInt" length="4">0</pc_usk>
  <pc_pegi_gen type="unsignedInt" length="4">0</pc_pegi_gen>
  <pc_pegi_fin type="unsignedInt" length="4">192</pc_pegi_fin>
  <pc_pegi_prt type="unsignedInt" length="4">0</pc_pegi_prt>
  <pc_pegi_bbfc type="unsignedInt" length="4">192</pc_pegi_bbfc>
  <pc_cob type="unsignedInt" length="4">0</pc_cob>
  <pc_grb type="unsignedInt" length="4">192</pc_grb>
  <pc_cgsrr type="unsignedInt" length="4">192</pc_cgsrr>
  <pc_oflc type="unsignedInt" length="4">0</pc_oflc>
  <pc_reserved0 type="unsignedInt" length="4">192</pc_reserved0>
  <pc_reserved1 type="unsignedInt" length="4">192</pc_reserved1>
  <pc_reserved2 type="unsignedInt" length="4">192</pc_reserved2>
  <pc_reserved3 type="unsignedInt" length="4">192</pc_reserved3>
  <ext_dev_nunchaku type="unsignedInt" length="4">0</ext_dev_nunchaku>
  <ext_dev_classic type="unsignedInt" length="4">0</ext_dev_classic>
  <ext_dev_urcc type="unsignedInt" length="4">0</ext_dev_urcc>
  <ext_dev_board type="unsignedInt" length="4">0</ext_dev_board>
  <ext_dev_usb_keyboard type="unsignedInt" length="4">0</ext_dev_usb_keyboard>
  <ext_dev_etc type="unsignedInt" length="4">0</ext_dev_etc>
  <ext_dev_etc_name type="string" length="512">EtcDevice</ext_dev_etc_name>
  <eula_version type="unsignedInt" length="4">0</eula_version>
  <drc_use type="unsignedInt" length="4">1</drc_use>
  <network_use type="unsignedInt" length="4">0</network_use>
  <online_account_use type="unsignedInt" length="4">0</online_account_use>
  <direct_boot type="unsignedInt" length="4">0</direct_boot>
  <reserved_flag0 type="hexBinary" length="4">00000000</reserved_flag0>
  <reserved_flag1 type="hexBinary" length="4">00000000</reserved_flag1>
  <reserved_flag2 type="hexBinary" length="4">00000000</reserved_flag2>
  <reserved_flag3 type="hexBinary" length="4">00000000</reserved_flag3>
  <reserved_flag4 type="hexBinary" length="4">00000000</reserved_flag4>
  <reserved_flag5 type="hexBinary" length="4">00000000</reserved_flag5>
  <reserved_flag6 type="hexBinary" length="4">00000000</reserved_flag6>
  <reserved_flag7 type="hexBinary" length="4">00000000</reserved_flag7>
{names("longname", long_name, 512)}
{names("shortname", short_name, 256)}
{names("publisher", publisher, 256)}
{addons}
</menu>
"""


def list_xml(list_type: str, demo_tid: str) -> str:
    return f"""<?xml version="1.0" encoding="utf-8"?>
<title_list type="{list_type}">
	<title order="1" start_date="2000-01-01 01:01:01" end_date="2038-12-31 23:59:59">{demo_tid}</title>
</title_list>
"""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print("wrote", path)


def write_if_missing(path: Path, text: str) -> None:
    if path.exists():
        print("kept ", path)
        return
    write(path, text)


def generate(slug: str) -> None:
    spec = TITLES[slug]
    release = REPO / "Release" / spec["unique"]
    write(release / "code" / "app.xml", app_xml(spec["tid"], spec["sdk_version"]))
    write(release / "code" / "cos.xml", cos_xml(spec["rpx"]))
    write(
        release / "meta" / "meta.xml",
        meta_xml(
            spec["tid"],
            spec["long_name"],
            spec["short_name"],
            PUBLISHER,
            spec["product_code"],
        ),
    )
    catalog = spec.get("list")
    if catalog:
        xml = list_xml(catalog["type"], catalog["placeholder"])
        write_if_missing(release / "meta" / catalog["filename"], xml)
        write_if_missing(REPO / spec["dir"] / "content" / catalog["filename"], xml)


def slug_from_project(project: Path) -> str:
    name = project.resolve().name
    if name in DIR_TO_SLUG:
        return DIR_TO_SLUG[name]
    raise SystemExit(
        f"Unknown project folder {project}. Expected one of: {', '.join(sorted(DIR_TO_SLUG))}"
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    slugs = ", ".join(sorted(TITLES))
    parser = argparse.ArgumentParser(
        description="Generate Cafe title XML into Release/<unique-id>/."
    )
    parser.add_argument(
        "title",
        nargs="?",
        help=f"Title slug or unique id ({slugs}, or 1fa82200). Default: all.",
    )
    parser.add_argument(
        "--project",
        type=Path,
        help="Title source folder (used by per-title wrappers).",
    )
    return parser.parse_args(argv)


def slugs_to_run(args: argparse.Namespace) -> list[str]:
    if args.project:
        return [slug_from_project(args.project)]
    if not args.title:
        return list(TITLES)
    key = args.title.strip().lower().replace(" ", "").replace("-", "")
    if key in TITLES:
        return [key]
    if key in UNIQUE_TO_SLUG:
        return [UNIQUE_TO_SLUG[key]]
    if args.title in DIR_TO_SLUG:
        return [DIR_TO_SLUG[args.title]]
    raise SystemExit(
        f"Unknown title {args.title!r}. Use one of: {', '.join(sorted(TITLES))}"
    )


def main(argv: list[str] | None = None) -> None:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    for slug in slugs_to_run(args):
        generate(slug)


if __name__ == "__main__":
    main()
