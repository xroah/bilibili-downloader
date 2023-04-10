import argparse

from ..cookie import cookie
from ..download.get_info import get_videos_by_bvid


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


def parse():
    parser = argparse.ArgumentParser(
        prog="Bilibili downloader",
        description="Download videos from bilibili.com"
    )
    subparsers = parser.add_subparsers()

    download_parser = subparsers.add_parser("download", aliases=["d"])
    download_parser.add_argument("bvid")

    cookie_parser = subparsers.add_parser("cookie", aliases=["c"])
    cookie_parser.add_argument("cookie", nargs="?")
    cookie_parser.add_argument(
        "-d",
        "--delete",
        action="store_true",
        dest="d"
    )

    args = parser.parse_args()
    _handle_cmd(args)

    return args
