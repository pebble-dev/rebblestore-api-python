import hashlib


def sha256_file(fname):
    hash_sha256 = hashlib.sha256()
    with open(fname, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()
