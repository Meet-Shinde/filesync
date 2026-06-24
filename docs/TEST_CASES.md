# FileSync MVP Test Cases

## Purpose

These tests prove sync correctness. They are more important than UI polish during MVP.

## NOW

### `test_full_file_sync.py`

Goal: prove basic two-client sync through the server.

Scenario:

1. Start server with clean database and storage.
2. Create Client A folder and Client B folder.
3. Client A creates `hello.txt`.
4. Client A uploads through sync runner.
5. Client B downloads through sync runner.
6. Assert Client B has the same file content.
7. Assert file hash matches.
8. Assert local metadata on both clients points to the same server version.

Expected result:

- File syncs from A to B without corruption.

## NEXT

### `test_conflict.py`

Goal: prove same-file edits do not silently overwrite.

Scenario:

1. Client A and Client B start with the same synced file.
2. Both clients modify the same file before syncing.
3. Client A syncs first.
4. Client B syncs after with an older `base_version_id`.
5. Server returns conflict.
6. Client B keeps its local version as a conflict copy.

Expected result:

- Both versions survive.
- Conflict metadata is recorded.

## MVP-LATER

### `test_chunk_upload.py`

Goal: prove server only asks for missing chunks.

Scenario:

1. Client chunks a file.
2. Client sends chunk hashes.
3. Server returns only missing hashes.
4. Client uploads missing chunks.

Expected result:

- Existing chunks are not re-uploaded.

### `test_deduplication.py`

Goal: prove duplicate chunks are stored once.

Scenario:

1. Two files contain identical chunk data.
2. Client uploads both files.
3. Server stores one copy of the shared chunk hash.

Expected result:

- Chunk storage is deduplicated by hash.

### `test_file_reconstruction.py`

Goal: prove downloaded chunks rebuild the original file.

Scenario:

1. Server has chunk metadata for a file version.
2. Client downloads chunks.
3. Client reconstructs the file.
4. Client verifies final full-file hash.

Expected result:

- Reconstructed file exactly matches original file.

### `test_rescan_detection.py`

Goal: prove periodic rescan catches changes missed by watcher.

Scenario:

1. Modify a file without relying on watcher event handling.
2. Run rescan.
3. Assert change detector marks file dirty.

Expected result:

- Missed changes are found by rescan.

### `test_server_restart.py`

Goal: prove server metadata survives restart.

Scenario:

1. Upload a file.
2. Stop and restart server.
3. Query metadata.
4. Download file.

Expected result:

- Metadata and stored files remain usable after restart.

## Test Rules

- Tests should use temporary folders.
- Tests should not depend on real personal files.
- Tests should clean up generated databases and storage.
- File content should be verified using hashes.
- Conflict tests must verify that no version is lost.
