from pathlib import Path
from dataclasses import dataclass 

@dataclass
class FileMetaData:
    relPath: str
    size: int
    mtime: float
    inode: int

def extract_metadata(path: Path, root: Path):
    stat = path.stat()

    metadata = FileMetaData(
        relPath = str(path.relative_to(root)),
        size = stat.st_size,
        mtime = stat.st_mtime,
        inode = stat.st_ino
    )

    return metadata

def iter_files(root: Path):
    files = []

    for path in root.rglob("*"):
        if path.is_file():
            files.append(path)

    return files

def scan_dir(root: Path):
    Record = []
    paths = iter_files(root)

    for path in paths:
        Record.append(extract_metadata(path,root))

    return Record


