from dataclasses import dataclass
from enum import Enum,auto

@dataclass
class FileMetaData:
    relPath: str
    size: int
    mtime: float
    inode: int
    hash: str | None = None

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
    
    def iter_changes(self):
        change_list = self.added + self.deleted + self.modified
        return change_list

class OperationType(Enum):
    UPLOAD = auto()
    DOWNLOAD = auto()
    DELETE = auto()

@dataclass
class Operation:
    type : OperationType
    file : FileMetaData

@dataclass
class Plan:
    operations : list[Operation]
