import json, base64, filecmp


def encode(fpath):
    with open(fpath, "rb") as f:
        in_bytes = f.read()
    file_string = base64.b64encode(in_bytes).decode("utf-8")
    return file_string


def decode(file_string, fpath):
    out_bytes = base64.b64decode(file_string.encode("utf-8"))
    with open(fpath, "wb") as f:
        f.write(out_bytes)