# FileSync

A desktop-first distributed file synchronization system.

## Goal

Sync selected folders between two desktop clients through a central FastAPI server.

## MVP

- FastAPI sync server
- Python local sync engine
- SQLite metadata
- File hashing
- Full-file sync first
- Chunked sync later
- Conflict-safe behavior
- Tauri + React desktop UI later

## Team

- Member 1: Backend, sync protocol, APIs, metadata, architecture
- Member 2: Local sync engine, scanner, hashing, chunking
- Member 3: Desktop UI, Tauri, React, TypeScript.
