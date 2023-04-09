import argparse

from ..cookie import cookie
from ..utils.request import get
from ..utils.encrypt_params import encrypt
from ..enums.Req import Req


def _handle_cmd(args: argparse.Namespace):
    if hasattr(args, "bvid"):
        # params = "avid=712020469&bvid=BV1wD4y1o7AS&cid=234725733&fnval=16&fnver=0&fourk=1&gaia_source=&qn=0"
        res = get(str(Req.VIEW_URL) + "?" + encrypt(f"bvid={args.bvid}"))
        print(res.json())
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
