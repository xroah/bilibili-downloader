import hashlib
import time
import random

_key = "e850e6b2063bb78bc7476d62fd0d4e72"

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