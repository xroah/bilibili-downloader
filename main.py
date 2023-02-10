import argparse
from downloader.utils.video_parser import get_episodes, get_info, get_video_page

if __name__ == "__main__":
    page = get_video_page("BV1r54y1m7gd")

    if page["code"] == 0:
        print(get_info(page["html_str"]))
        print(get_episodes(page["html_str"]))
    else:
        print(page["msg"])
