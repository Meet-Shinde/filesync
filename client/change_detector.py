from dataclasses import dataclass
from scanner import FileMetaData
from enum import Enum

class ChangeType(Enum):
    ADDED = 1
    DELETED = 2
    MODIFIED = 3
    UNCHANGED = 4

@dataclass
class Change:
    change_type: ChangeType
    old_metadata: FileMetaData | None
    new_metadata: FileMetaData | None

@dataclass
class ChangeSet:
    added: list[Change]
    deleted: list[Change]
    modified: list[Change]
    unchanged: list[Change]

def build_lookup(data: list[FileMetaData]):

    lookup_table = {
        file.relpath : file 
        for file in data 
    }

    return lookup_table

