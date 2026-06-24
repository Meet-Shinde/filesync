# FileSync Architecture

## Overview

FileSync uses a desktop-client plus central-server architecture for the MVP.

Each desktop client watches or scans a selected local folder, records local metadata in SQLite, compares local state with the server, uploads local changes, downloads remote changes, and handles conflicts safely.

The central server stores metadata and file data. For the MVP, the server uses SQLite and local filesystem storage.

## Main Components

| Component | Folder | Owner | Responsibility |
| Backend server | `backend/` | Person 1 | FastAPI APIs, server metadata, file/chunk storage, sync decisions, conflict API |
| Local sync engine | `client/` | Person 2 | Scanning, hashing, local DB, change detection, upload/download planning, chunking later |
| Desktop app | `desktop/` | Person 3 | Tauri + React + TypeScript UI for folder selection, status, progress, conflicts, and errors |
| Tests | `tests/` | Shared | End-to-end correctness tests for sync behavior |
| Docs | `docs/` | Shared, Person 1 primary | Source of truth for architecture, protocol, APIs, schema, scope, and tests |

## MVP Data Flow

Phase 1 uses full-file sync first.

1. User selects a folder in the desktop app.
2. Local sync engine scans files in that folder.
3. Client computes file hashes.
4. Client stores local file state in SQLite.
5. Client asks the server for remote metadata.
6. Sync planner decides whether each file needs upload, download, conflict handling, or no action.
7. Client uploads full files to the server.
8. Server stores file data and updates metadata.
9. Other clients download remote changes.
10. Client verifies downloaded file hash and updates local metadata.

Chunked sync is added later in the MVP after full-file sync is proven.

## Storage Model

Server-side storage:

- Metadata lives in SQLite.
- Uploaded file data lives under `backend/storage/objects/`.
- Temporary upload data lives under `backend/storage/tmp/`.
- Database files and stored objects are not committed to Git.

Client-side storage:

- Client metadata lives in local SQLite.
- The selected sync folder contains the user's real files.
- Local sync metadata should be stored outside the synced folder or in an ignored `.filesync/` directory.

## Conflict Strategy

The MVP does not attempt smart merging.

If two clients modify the same file before syncing, FileSync keeps both versions:

- One version keeps the original path.
- The other version is saved as a conflict copy.
- Metadata records the conflict so the UI can display it.

This protects against silent overwrites.

## Final MVP Repository Structure

```txt
filesync/
|-- docs/
|   |-- ARCHITECTURE.md              [NOW]
|   |-- SYNC_PROTOCOL.md             [NOW]
|   |-- API_CONTRACT.md              [NOW]
|   |-- DATABASE_SCHEMA.md           [NOW]
|   |-- MVP_SCOPE.md                 [NOW]
|   `-- TEST_CASES.md                [NOW]
|-- backend/
|   |-- app/
|   |   |-- __init__.py              [NOW]
|   |   |-- main.py                  [NOW]
|   |   |-- config.py                [NOW]
|   |   |-- database.py              [NOW]
|   |   |-- models.py                [NOW]
|   |   |-- schemas.py               [NOW]
|   |   |-- storage.py               [NOW]
|   |   |-- hashing.py               [NOW]
|   |   |-- routers/
|   |   |   |-- __init__.py          [NOW]
|   |   |   |-- devices.py           [NOW]
|   |   |   |-- sync_spaces.py       [NOW]
|   |   |   |-- files.py             [NOW]
|   |   |   `-- chunks.py            [MVP-LATER]
|   |   `-- services/
|   |       |-- __init__.py          [NOW]
|   |       |-- sync_service.py      [NOW]
|   |       |-- conflict_service.py  [NEXT]
|   |       |-- file_service.py      [NOW]
|   |       `-- chunk_service.py     [MVP-LATER]
|   |-- storage/
|   |   |-- tmp/.gitkeep            [NOW]
|   |   `-- objects/.gitkeep        [NOW]
|   |-- requirements.txt            [NOW]
|   `-- README.md                   [NOW]
|-- client/
|   |-- __init__.py                 [NOW]
|   |-- config.py                   [NOW]
|   |-- scanner.py                  [NOW]
|   |-- hasher.py                   [NOW]
|   |-- local_db.py                 [NOW]
|   |-- change_detector.py          [NOW]
|   |-- sync_planner.py             [NOW]
|   |-- api_client.py               [NOW]
|   |-- sync_runner.py              [NOW]
|   |-- conflict_handler.py         [NEXT]
|   |-- watcher.py                  [MVP-LATER]
|   |-- rescan.py                   [MVP-LATER]
|   |-- chunker.py                  [MVP-LATER]
|   |-- chunk_manifest.py           [MVP-LATER]
|   |-- file_reconstructor.py       [MVP-LATER]
|   |-- transfer_queue.py           [MVP-LATER]
|   `-- benchmark.py                [MVP-LATER]
|-- desktop/
|   `-- README.md                   [NOW]
|-- tests/
|   |-- test_full_file_sync.py      [NOW]
|   |-- test_conflict.py            [NEXT]
|   |-- test_chunk_upload.py        [MVP-LATER]
|   |-- test_deduplication.py       [MVP-LATER]
|   |-- test_file_reconstruction.py [MVP-LATER]
|   |-- test_rescan_detection.py    [MVP-LATER]
|   `-- test_server_restart.py      [MVP-LATER]
|-- .gitignore                      [NOW]
|-- README.md                       [NOW]
`-- requirements.txt                [NOW]
```

## Architecture Rule

The backend should not directly inspect the user's local folders. The client owns filesystem scanning and local file operations. The server owns shared metadata, storage, and API-level correctness.
