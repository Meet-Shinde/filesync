# FileSync MVP Scope

## Project Identity

FileSync is a desktop-first distributed file sync system. The MVP proves that two desktop clients can safely sync one selected folder through a central FastAPI server without data loss.

The goal is to build a reliable sync engine, not a Dropbox or Google Drive clone.

## MVP Success Definition

The MVP is successful when:

- Client A selects a local folder.
- Client B selects a local folder.
- Both clients register with the central server.
- A file created or modified on Client A appears correctly on Client B.
- A file created or modified on Client B appears correctly on Client A.
- Local metadata and server metadata stay consistent.
- Same-file edits on two clients do not silently overwrite each other.
- The system can demonstrate at least one safe conflict copy.

## Included In MVP

### Phase 1: NOW

- FastAPI backend server.
- SQLite server database.
- Local client SQLite database.
- Device registration.
- Sync space creation.
- Full-file hashing.
- Folder scanning.
- Change detection using local metadata.
- Full-file upload.
- Full-file download.
- Basic sync runner.
- Basic integration test for two-client full-file sync.

### Phase 2: NEXT

- Conflict detection.
- Conflict copy behavior.
- Improved sync planner rules.
- Conflict test case.

### Phase 3: MVP-LATER

- Fixed-size chunking.
- Chunk hashing.
- Chunk manifest generation.
- Missing-chunk check.
- Upload only missing chunks.
- File reconstruction from chunks.
- Deduplication by chunk hash.

### Phase 4: MVP-LATER

- Folder watcher.
- Periodic rescan.
- Transfer queue and retry handling.
- Server restart test.
- Rescan detection test.
- Basic benchmarking for scanning, hashing, and chunking.

## Excluded From MVP

The following are intentionally out of scope:

- LAN sync.
- Peer-to-peer sync.
- End-to-end encryption.
- Production authentication.
- Role-based team permissions.
- Cloud object storage such as S3 or MinIO.
- Content-defined chunking.
- Real-time collaboration.
- Smart merge of file conflicts.
- Mobile app.
- Kubernetes or production deployment.

## Team Ownership

Person 1 owns backend, sync protocol, server database schema, API contract, conflict service, storage correctness, and integration tests.

Person 2 owns the local sync engine in `client/`: scanning, hashing, local metadata, change detection, sync planning, API client integration, conflict file behavior, watcher/rescan, chunking, reconstruction, transfer queue, and benchmarking.

Person 3 owns the desktop application in `desktop/`: Tauri + React + TypeScript UI, folder selection, sync status, progress, conflicts, errors, retries, and device/server status.

## Project Principle

Correctness over features.

The system must prefer safe behavior over clever behavior. If the system is unsure whether a file should be overwritten, it must create a conflict copy instead of risking data loss.
