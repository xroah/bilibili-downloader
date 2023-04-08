from downloader.utils.video_parser import get_episodes, get_info, get_video_page
from downloader.cli import cli
from downloader.server.server import run_server

if __name__ == "__main__":
    args = cli.parse()

    if not hasattr(args, "bvid"):
        run_server()
    else:
        page = get_video_page(args.bvid)

        print(get_info(page["html_str"]))
