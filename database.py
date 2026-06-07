import sqlite3
import json

class DatabaseManager:

    def __init__(self):
        self.conn = sqlite3.connect("data/memoryos.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS files (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                path TEXT UNIQUE,
                                filename TEXT,
                                file_size INTEGER,
                                modified_time REAL,
                                file_hash TEXT,
                                content TEXT
                            )
                            """)

        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS chunks (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                file_id INTEGER,
                                chunk_number INTEGER,
                                chunk_text TEXT
                            )
                            """)
        
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS embeddings(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                chunk_id INTEGER,
                                embedding TEXT 
                            )
                            """)
        self.conn.commit()

    def insert_file(
        self,
        path,
        filename,
        file_size,
        modified_time,
        file_hash,
        content
    ):
        self.cursor.execute("""
                            INSERT OR REPLACE INTO files
                            (
                                path,
                                filename,
                                file_size,
                                modified_time,
                                file_hash,
                                content
                            )
                            VALUES (?, ?, ?, ?, ?, ?)
                            """,
                            (
                                path,
                                filename,
                                file_size,
                                modified_time,
                                file_hash,
                                content
                            ))
        self.conn.commit()

    def get_file_by_path(self, path):
        self.cursor.execute("""
                            SELECT file_hash
                            FROM files
                            WHERE path = ?
                            """, (path,))
        return self.cursor.fetchone()

    def get_file_id(self, path):
        self.cursor.execute("""
                            SELECT id
                            FROM files
                            WHERE path = ?
                            """, (path,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def insert_chunk(
        self,
        file_id,
        chunk_number,
        chunk_text
    ):
        self.cursor.execute("""
                            INSERT INTO chunks
                            (
                                file_id,
                                chunk_number,
                                chunk_text
                            )
                            VALUES (?, ?, ?)
                            """,
                            (
                                file_id,
                                chunk_number,
                                chunk_text
                            ))
        self.conn.commit()
        
    def delete_chunks(self, file_id):
        self.cursor.execute('''
                            DELETE FROM chunks
                            WHERE file_id = ?
                            ''', (file_id,))
        self.conn.commit()
        
    def count_chunks(self):
        self.cursor.execute("""
                            SELECT COUNT(*)
                            FROM chunks
                            """)
        return self.cursor.fetchone()[0]

    def get_all_chunks(self):
        self.cursor.execute('''
                            SELECT id, chunk_text
                            FROM chunks
                            ''')
        return self.cursor.fetchall()
    
    def get_chunk_by_id(self, chunk_id):
        self.cursor.execute('''
                            SELECT chunk_text
                            FROM chunks
                            WHERE id = ?
                            ''', (chunk_id,))
        result =  self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def get_chunk_details(self, chunk_id):
        self.cursor.execute('''
                            SELECT chunks.chunk_text, files.filename
                            FROM chunks
                            JOIN files
                            ON chunks.file_id = files.id
                            WHERE chunks.id = ?
                            ''', (chunk_id,))
        return self.cursor.fetchone()
    
    def search_files(self, query):
        self.cursor.execute("""
                            SELECT filename, path, content
                            FROM files
                            WHERE content LIKE ?
                            """, (f"%{query}%",))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
        
        
    def insert_embedding(self, chunk_id, embedding):
        embedding_json = json.dumps(embedding.tolist())
        self.cursor.execute("""
                            INSERT INTO embeddings(chunk_id, embedding)
                            VALUES (?, ?)
                            """, (chunk_id, embedding_json))
        self.conn.commit()
        
    def get_file_info_from_chunk(
        self,
        chunk_id
    ):

        self.cursor.execute("""
            SELECT
                files.filename,
                files.path,
                chunks.chunk_text

            FROM chunks

            JOIN files
            ON chunks.file_id = files.id

            WHERE chunks.id = ?
        """, (chunk_id,))

        return self.cursor.fetchone()
    
    def keyword_search(self, query):
        self.cursor.execute('''
                            SELECT chunks.id, chunks.chunk_text, files.filename, files.path
                            FROM chunks
                            JOIN files ON chunks.file_id = files.id
                            WHERE chunks.chunk_text LIKE ?
                            ''', (f"%{query}%",))
        return self.cursor.fetchall()
    
    
    
    
