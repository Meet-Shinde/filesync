import hashlib
from models import FileMetaData

def hash_file(path , fileinfo: FileMetaData):
    hasher = hashlib.sha256()

    for chunk in read_chunks(path):
        hasher.update(chunk)

    fileinfo.hash = hasher.hexdigest()

    return fileinfo

def read_chunks(path):
    with open(path, "rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            yield chunk