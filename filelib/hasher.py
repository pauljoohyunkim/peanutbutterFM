import hashlib

def sha256sum(filepath, block=2**32):
    hasher = hashlib.sha256()
    with open(filepath, "rb") as file:
        read_bytes = file.read(block)
        while read_bytes:
            hasher.update(read_bytes)
            read_bytes = file.read(block)
    return hasher.hexdigest()
