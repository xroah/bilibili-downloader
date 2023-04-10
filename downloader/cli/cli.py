import argparse

from ..cookie import cookie
from ..download.get_info import get_videos_by_bvid
from ..settings import settings


def _handle_cmd(args: argparse.Namespace):
    if hasattr(args, "bvid"):
        ret = get_videos_by_bvid(args.bvid)
        print(ret)
    elif hasattr(args, "cookie"):
        if args.d:
            cookie.delete()
        elif args.cookie is not None:
            cookie.set(args.cookie)
        else:
            print(cookie.cookie)
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
    download_parser.add_argument("bvid")

    cookie_parser = subparsers.add_parser(
        "cookie",
        description="Get or set cookies"
    )
    cookie_parser.add_argument("cookie", nargs="?")
    cookie_parser.add_argument(
        "-d",
        "--delete",
        action="store_true",
        dest="d"
    )

    config_parser = subparsers.add_parser(
        "config",
        description="Get or set settings"
    )
    config_parser.add_argument("settings", nargs="+")

    args = parser.parse_args()
    
    _handle_cmd(args)

    return args
