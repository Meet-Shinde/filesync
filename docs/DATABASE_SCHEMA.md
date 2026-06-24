# FileSync Database Schema

## Overview

The MVP uses SQLite on both server and client.

Server database:

- Tracks devices, sync spaces, file records, file versions, and later chunks.

Client database:

- Tracks local file state, known server versions, pending work, conflicts, and later chunk manifests.

This schema is a starting MVP schema. It can be refined during implementation, but changes should keep the same concepts.

## Server Database

### `devices`

| Column | Type | Notes |
| `id` | TEXT PRIMARY KEY | Unique `device_id` |
| `name` | TEXT | Human-readable device name |
| `created_at` | TEXT | ISO timestamp |
| `last_seen_at` | TEXT | ISO timestamp |

### `sync_spaces`

| Column | Type | Notes |
| `id` | TEXT PRIMARY KEY | Unique sync folder group |
| `name` | TEXT | Display name |
| `created_at` | TEXT | ISO timestamp |

### `files`

One row per logical path in a sync space.

| Column | Type | Notes |
| `id` | TEXT PRIMARY KEY | File record ID |
| `sync_space_id` | TEXT | References `sync_spaces.id` |
| `relative_path` | TEXT | Path inside synced folder |
| `current_version_id` | TEXT | Latest active version |
| `deleted` | INTEGER | `0` or `1` tombstone flag |
| `created_at` | TEXT | ISO timestamp |
| `updated_at` | TEXT | ISO timestamp |

Unique constraint:

```sql
UNIQUE(sync_space_id, relative_path)
```

### `file_versions`

One row per uploaded version of a file.

| Column | Type | Notes |
| `id` | TEXT PRIMARY KEY | Version ID |
| `file_id` | TEXT | References `files.id` |
| `device_id` | TEXT | Device that created this version |
| `base_version_id` | TEXT NULL | Client's previous known version |
| `file_hash` | TEXT | SHA-256 full-file hash |
| `size_bytes` | INTEGER | File size |
| `storage_path` | TEXT | Object path for full-file phase |
| `created_at` | TEXT | ISO timestamp |

### `chunks` MVP-LATER

One row per unique chunk hash.

| Column | Type | Notes |
| `hash` | TEXT PRIMARY KEY | SHA-256 chunk hash |
| `size_bytes` | INTEGER | Chunk size |
| `storage_path` | TEXT | Object path |
| `created_at` | TEXT | ISO timestamp |

### `file_version_chunks` MVP-LATER

Maps a file version to its chunks.

| Column | Type | Notes |
| `file_version_id` | TEXT | References `file_versions.id` |
| `chunk_hash` | TEXT | References `chunks.hash` |
| `chunk_index` | INTEGER | Order in file |
| `offset_bytes` | INTEGER | Start offset |
| `size_bytes` | INTEGER | Chunk size |

Unique constraint:

```sql
UNIQUE(file_version_id, chunk_index)
```

## Client Database

### `local_files`

Tracks the client's local view of each synced file.

| Column | Type | Notes |
| `relative_path` | TEXT PRIMARY KEY | Path inside selected folder |
| `file_hash` | TEXT | Last known local hash |
| `size_bytes` | INTEGER | Last known size |
| `modified_time` | TEXT | Filesystem modified time |
| `server_version_id` | TEXT NULL | Last synced server version |
| `sync_status` | TEXT | `synced`, `dirty`, `pending`, `conflict`, `deleted` |
| `deleted` | INTEGER | `0` or `1` |
| `last_scanned_at` | TEXT | ISO timestamp |
| `last_synced_at` | TEXT NULL | ISO timestamp |

### `pending_transfers`

Tracks work that has not completed yet.

| Column | Type | Notes |
| `id` | TEXT PRIMARY KEY | Transfer ID |
| `relative_path` | TEXT | File path |
| `direction` | TEXT | `upload` or `download` |
| `status` | TEXT | `pending`, `running`, `failed`, `done` |
| `retry_count` | INTEGER | Retry attempts |
| `error_message` | TEXT NULL | Last error |
| `created_at` | TEXT | ISO timestamp |
| `updated_at` | TEXT | ISO timestamp |

### `conflicts`

Tracks conflict copies for UI and debugging.

| Column | Type | Notes |
| `id` | TEXT PRIMARY KEY | Conflict ID |
| `relative_path` | TEXT | Original file path |
| `conflict_path` | TEXT | Local conflict copy path |
| `local_hash` | TEXT | Local version hash |
| `server_version_id` | TEXT | Conflicting server version |
| `created_at` | TEXT | ISO timestamp |
| `resolved` | INTEGER | `0` or `1` |

### `local_chunks` MVP-LATER

Tracks local chunk manifests.

| Column | Type | Notes |
| `relative_path` | TEXT | File path |
| `file_hash` | TEXT | Full file hash |
| `chunk_index` | INTEGER | Chunk order |
| `chunk_hash` | TEXT | SHA-256 chunk hash |
| `offset_bytes` | INTEGER | Start offset |
| `size_bytes` | INTEGER | Chunk size |

## Schema Rules

- Store timestamps in ISO 8601 text format.
- Use SHA-256 for file and chunk hashes.
- Do not use absolute local paths in server metadata.
- Use `relative_path` for sync identity.
- Treat deletes as tombstones.
- Do not mark files as synced until disk write and hash verification succeed.
