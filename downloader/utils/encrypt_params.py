import hashlib
import time
import random

_key = "86217b4772916fc323ce3b38264b4773"


def md5(data: str) -> str:
    m = hashlib.new("md5")
    m.update(data.encode())

    return m.hexdigest()


def encrypt(params: str) -> str:
    session = md5(str(random.random()))
    params_with_session = f"{params}&session={session}"
    wts = round(time.time())
    w_rid = md5(f"{params_with_session}&wts={wts}{_key}")

    return f"{params_with_session}&w_rid={w_rid}&wts={wts}"
