from downloader.cli import cli
from downloader.server.server import run_server
from downloader.utils.encrypt_params import encrypt
from downloader.utils.request import get
from downloader.enums import Req


if __name__ == "__main__":
    args = cli.parse()

    if not hasattr(args, "bvid"):
        run_server()
    else:
        # params = "avid=712020469&bvid=BV1wD4y1o7AS&cid=234725733&fnval=16&fnver=0&fourk=1&gaia_source=&qn=80"
        # final_params = encrypt(params)
        # res = get(str(Req.PLAY_URL) + "?" + final_params)

        # print(res.json())
        res = get(str(Req.VIEW_URL) + "?" + encrypt("bvid=BV1r54y1m7gd"))

        print(res.json())