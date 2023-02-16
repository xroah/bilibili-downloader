import argparse


def parse():
    parser = argparse.ArgumentParser(
        prog="Bilibili downloader",
        description="Download videos from bilibili.com"
    )
    subparsers = parser.add_subparsers()
    parser_d = subparsers.add_parser("d")

    parser_d.add_argument("bvid")

    args = parser.parse_args()

    return args
