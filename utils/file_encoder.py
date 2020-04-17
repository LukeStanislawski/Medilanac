import json
import base64
import filecmp


def encode(fpath):
    """
    Encode file at a given filepath into bas64 chars

    fpath: File path of file to be encoded
    """
    with open(fpath, "rb") as f:
        in_bytes = f.read()
    file_string = base64.b64encode(in_bytes).decode("utf-8")
    return file_string


def decode(file_string, fpath):
    """
    Decodes base64 string to a file at a given filepath

    file_string: Base64 string of file data to be decoded
    fpath: File path of location to write file too
    """
    out_bytes = base64.b64decode(file_string.encode("utf-8"))
    with open(fpath, "wb") as f:
        f.write(out_bytes)