import argparse

from ..download.get_info import get_videos_by_bvid
from ..download.Download import Download
from ..settings import settings


def _handle_cmd(args: argparse.Namespace):
    if hasattr(args, "bvid"):
        if args.bvid is None:
            pass
        else:
            ret = get_videos_by_bvid(args.bvid)
            Download(ret)
    elif hasattr(args, "settings"):
        settings_args = args.settings
        print(args)
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

    config_parser = subparsers.add_parser(
        "config",
        description="Get or set configurations"
    )
    config_parser.add_argument("settings", nargs="+")

    args = parser.parse_args()

    _handle_cmd(args)

    return args
