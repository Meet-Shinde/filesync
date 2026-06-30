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

def detect_changes(current_data : list[FileMetaData] , previous_data : list[FileMetaData]):

    current_lookup = build_lookup(current_data)
    previous_lookup = build_lookup(previous_data)

    added = detect_added(current_lookup, previous_lookup)
    deleted = detect_deleted(current_lookup, previous_lookup)
    modified , unchanged = detect_modified_and_unchanged(current_lookup, previous_lookup)

    final_change = ChangeSet(
        added = added,
        deleted = deleted,
        modified = modified,
        unchanged = unchanged
    )

    return final_change

def build_lookup(data: list[FileMetaData]):

    lookup_table = {
        file.relpath : file 
        for file in data 
    }

    return lookup_table

def detect_added(curr_lookup : dict , old_lookup : dict):

    added_changes = []

    for path in curr_lookup:
        if path not in old_lookup:
            new_file = Change(
                change_type = ChangeType.ADDED,
                old_metadata = None,
                new_metadata = curr_lookup[path]
            )
            
            added_changes.append(new_file)

    return added_changes

def detect_deleted(curr_lookup : dict , old_lookup : dict):

    deleted_changes = []

    for path in old_lookup:
        if path not in curr_lookup:
            new_file = Change(
                change_type = ChangeType.DELETED,
                old_metadata = old_lookup[path],
                new_metadata = None
            )
            
            deleted_changes.append(new_file)

    return deleted_changes

def detect_modified_and_unchanged(curr_lookup : dict , old_lookup : dict):

    modified_changes = []
    unchanged = []

    def create_change():
        new_file = Change(
        change_type = ChangeType.MODIFIED,
        old_metadata = old_lookup[path],
        new_metadata = curr_lookup[path]
    )
        modified_changes.append(new_file)
        

    for path in curr_lookup:
        if path in old_lookup:
            if curr_lookup[path].size != old_lookup[path].size:
                create_change()
            elif curr_lookup[path].mtime != old_lookup[path].mtime:
                create_change()
            elif curr_lookup[path].hash != old_lookup[path].hash:
                create_change()
            else:
                new_file = Change(
                change_type = ChangeType.UNCHANGED,
                old_metadata = old_lookup[path],
                new_metadata = curr_lookup[path]
                )

                unchanged.append(new_file)


    return modified_changes,unchanged
