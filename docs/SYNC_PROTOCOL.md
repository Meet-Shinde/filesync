# FileSync Sync Protocol

## Goal

The sync protocol defines how clients and the server decide what to upload, download, skip, or mark as a conflict.

The MVP starts with full-file sync. Chunked sync is added later after the full-file path works reliably.

## Core Identifiers

| Identifier | Meaning |
| `device_id` | Unique ID for one desktop client installation |
| `sync_space_id` | One shared synced folder group |
| `relative_path` | File path inside the selected sync folder |
| `file_hash` | SHA-256 hash of the full file contents |
| `version_id` | Server-created ID for one file version |
| `base_version_id` | Last server version known by the client before making a local change |
| `deleted` | Boolean/tombstone state showing that a file was deleted |

## Phase 1: Full-File Sync

### Upload Flow

1. Client scans the selected folder.
2. Client computes file hash for each file.
3. Client compares scan result with local SQLite metadata.
4. Client asks server for current metadata for the sync space.
5. Client decides which files are new or modified locally.
6. Client uploads the full file with metadata:
   - `device_id`
   - `sync_space_id`
   - `relative_path`
   - `file_hash`
   - `size_bytes`
   - `modified_time`
   - `base_version_id`
7. Server validates the upload.
8. Server creates a new file version if safe.
9. Client records the returned `version_id` in local SQLite.

### Download Flow

1. Client asks server for remote changes since last sync.
2. Server returns file metadata and download references.
3. Client downloads files that are missing or outdated locally.
4. Client writes downloads safely using a temporary file first.
5. Client verifies the downloaded file hash.
6. Client atomically replaces the local file.
7. Client updates local SQLite metadata.

## Sync Decisions

| Local state | Server state | Decision |
| Same hash and same version | Same | No action |
| Local file changed, server unchanged from base | Older/same base | Upload |
| Local unchanged, server has newer version | Newer | Download |
| Local changed, server also changed from base | Newer/different | Conflict |
| Local file missing, server has active file | Active | Download unless local deletion is confirmed |
| Local deletion, server unchanged from base | Same base | Upload delete/tombstone |
| Local deletion, server changed | Newer/different | Conflict |

## Conflict Rule

The MVP must never silently overwrite a local changed file.

When both client and server have different changes after the same base version:

1. Keep the server version at the original path or download it safely.
2. Preserve the local version as a conflict copy.
3. Mark the file as conflicted in local metadata.
4. Let the desktop UI show the conflict.

Suggested conflict filename:

```txt
filename (conflict from DEVICE_ID YYYY-MM-DD-HHMMSS).ext
```

## Delete Rule

Deletes should be represented as metadata tombstones, not only as missing files.

For MVP:

- Do not permanently erase server metadata immediately.
- Record `deleted = true`.
- Keep enough metadata to sync the deletion to other clients.
- If one client deletes a file while another modifies it, treat it as a conflict.

## Phase 3: Chunked Sync Later

Chunked sync is MVP-LATER.

When added:

1. Client splits file into fixed-size chunks.
2. Client computes SHA-256 hash for each chunk.
3. Client sends chunk manifest to server.
4. Server replies with missing chunk hashes.
5. Client uploads only missing chunks.
6. Server commits file version after all required chunks exist.
7. Downloading client reconstructs file from chunks.
8. Client verifies final full-file hash.

## Safety Rules

- Use temporary files for downloads before replacing real files.
- Verify hashes after upload/download.
- Do not update local metadata as synced until the file operation succeeds.
- Do not create server metadata for a completed version until upload data is valid.
- Prefer conflict copy over overwrite when uncertain.
- Watcher events are not trusted alone; periodic rescan is required later.
