import argparse

from ..download.get_info import get_videos
from ..download.history import print_downloaded_videos
from ..settings import settings
from ..download.Download import Download


def _handle_cmd(args: argparse.Namespace):
    if hasattr(args, "bvid"):
        if args.history:
            print_downloaded_videos()
            return
        if args.bvid is not None:
            get_videos(args.bvid, args.no_season)
        Download()
    elif hasattr(args, "settings"):
        settings_args = args.settings

        if len(settings_args) > 1:
            settings.set(settings_args[0], settings_args[1])
        else:
            v = settings.get(settings_args[0])
            print(v if v is not None else "")


def parse():
    parser = argparse.ArgumentParser(
        prog="Bilibili downloader",
        description="Download videos from bilibili.com"
    )
    subparsers = parser.add_subparsers()

    download_parser = subparsers.add_parser(
        "download",
        aliases=["d"],
        description="Download videos"
    )
    download_parser.add_argument("bvid", nargs="?")
    download_parser.add_argument(
        "--no-season",
        "-S",
        action="store_true",
    )
    download_parser.add_argument(
        "--history",
        "-H",
        action="store_true"
    )

    config_parser = subparsers.add_parser(
        "config",
        aliases=["c"],
        description="Get or set configurations"
    )
    config_parser.add_argument("settings", nargs="+")

    args = parser.parse_args()

    _handle_cmd(args)

    return args
