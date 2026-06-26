import sqlite3
from scanner import FileMetaData  

class LocalDB:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = self._connect(db_name)
        self._create_tables()

    def _connect(self, db_name):
        conn = sqlite3.connect(db_name)
        self.cursor = conn.cursor()
        return conn

    def _create_tables(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS files (
            path TEXT PRIMARY KEY,
            size INTEGER,
            mtime REAL,
            inode INTEGER
            )
            """
        )
        self.conn.commit()

    def upsert_file(self, data):
        self.cursor.execute(
        """
        INSERT INTO files (path,size,mtime,inode)
        VALUES (?,?,?,?)
        ON CONFLICT(path) DO UPDATE SET
        size = excluded.size,
        mtime = excluded.mtime,
        inode = excluded.inode
        """,
        (
            str(data.relPath),  
            data.size,
            data.mtime,  
            data.inode,
        )
    )
        
    def save_snapshot(self, records):
        self.clear()

        for record in records:
            self.upsert_file(record)

        self.conn.commit()

    def get_file(self, root):
        self.cursor.execute("SELECT * FROM files WHERE path = ?",
        (root,)
        )
        row = self.cursor.fetchone()

        if row is None:
            return None
        
        path, size, mtime, inode = row

        return FileMetaData(
            relPath = path,
            size = size,
            mtime = mtime,
            inode = inode 
        ) 
    
    def get_all_files(self):
        self.cursor.execute("SELECT * FROM files"
        )
        rows = self.cursor.fetchall()

        records = []

        for row in rows:
            path, size, mtime, inode = row
            records.append(
                FileMetaData(
                    relPath = path,
                    size = size,
                    mtime = mtime,
                    inode = inode
                )
            )
        return records
    
    def delete_file(self, path):
        self.cursor.execute("DELETE FROM files WHERE path = ?",
        (path,)
        )
        self.conn.commit()

    def clear(self):
        self.cursor.execute("DELETE FROM files")

    def close(self):
        self.conn.close()