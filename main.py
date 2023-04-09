from downloader.cli import cli
from downloader.server.server import run_server


if __name__ == "__main__":
    args = vars(cli.parse())

    if len(args.keys()) == 0:
        run_server()
