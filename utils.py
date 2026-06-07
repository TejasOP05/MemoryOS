import hashlib


def calculate_hash(file_path):

    hasher = hashlib.md5()

    with open(file_path, "rb") as f:

        while chunk := f.read(4096):

            hasher.update(chunk)

    return hasher.hexdigest()