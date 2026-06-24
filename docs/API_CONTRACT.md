# FileSync API Contract

## Overview

The backend API is owned by Person 1. Person 2 and Person 3 should treat this document as the contract for client and desktop integration.

The MVP starts with full-file sync. Chunk endpoints exist in the plan but are MVP-LATER.

Base URL for local development:

```txt
http://127.0.0.1:8000
```

## Health

### `GET /health`

Returns server status.

Response:

```json
{
  "status": "ok"
}
```

## Devices

### `POST /devices`

Registers a desktop client.

Request:

```json
{
  "name": "Laptop"
}
```

Response:

```json
{
  "device_id": "dev_123",
  "name": "Laptop"
}
```

### `GET /devices`

Returns registered devices.

## Sync Spaces

### `POST /sync-spaces`

Creates a shared sync space.

Request:

```json
{
  "name": "My Synced Folder"
}
```

Response:

```json
{
  "sync_space_id": "space_123",
  "name": "My Synced Folder"
}
```

### `GET /sync-spaces`

Returns available sync spaces.

## File Metadata

### `GET /sync-spaces/{sync_space_id}/files`

Returns current server file metadata for a sync space.

Response:

```json
{
  "files": [
    {
      "relative_path": "notes/todo.txt",
      "version_id": "ver_123",
      "file_hash": "sha256...",
      "size_bytes": 1200,
      "deleted": false,
      "updated_at": "2026-06-24T12:00:00Z"
    }
  ]
}
```

## Full-File Upload: NOW

### `POST /sync-spaces/{sync_space_id}/files/upload`

Uploads a full file in Phase 1.

Request type:

```txt
multipart/form-data
```

Fields:

| Field | Meaning |
| `device_id` | Uploading device |
| `relative_path` | Path inside sync folder |
| `file_hash` | SHA-256 full-file hash |
| `size_bytes` | File size |
| `modified_time` | Client filesystem modified time |
| `base_version_id` | Last known server version, nullable |
| `file` | File content |

Success response:

```json
{
  "status": "uploaded",
  "relative_path": "notes/todo.txt",
  "version_id": "ver_124",
  "file_hash": "sha256..."
}
```

Conflict response:

```json
{
  "status": "conflict",
  "relative_path": "notes/todo.txt",
  "server_version_id": "ver_123",
  "reason": "server changed since base_version_id"
}
```

## Full-File Download: NOW

### `GET /sync-spaces/{sync_space_id}/files/download`

Downloads a full file by path or version.

Query parameters:

| Parameter | Meaning |
| `relative_path` | File path inside sync folder |
| `version_id` | Optional exact version |

Response:

```txt
application/octet-stream
```

The client must verify the downloaded hash before replacing the local file.

## Delete: NEXT

### `POST /sync-spaces/{sync_space_id}/files/delete`

Creates a delete tombstone.

Request:

```json
{
  "device_id": "dev_123",
  "relative_path": "notes/todo.txt",
  "base_version_id": "ver_123"
}
```

Response:

```json
{
  "status": "deleted",
  "relative_path": "notes/todo.txt",
  "version_id": "ver_125"
}
```

## Chunk Endpoints: MVP-LATER

### `POST /sync-spaces/{sync_space_id}/chunks/check`

Client sends chunk hashes. Server returns missing hashes.

### `POST /sync-spaces/{sync_space_id}/chunks/upload`

Client uploads missing chunks.

### `POST /sync-spaces/{sync_space_id}/files/commit-chunks`

Client commits a file version after required chunks exist on the server.

## API Rules

- All paths are relative to the selected sync folder.
- The server must reject unsafe paths such as `../secret.txt`.
- The server must verify file hash after upload.
- Conflict responses must be explicit.
- Client must not treat failed or conflicted uploads as synced.
