import os
import sqlite3
from datetime import datetime

DB_NAME = 'logs.db'
DB_PATH = os.path.join('db', DB_NAME)

def setup_database():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY,
                session_id TEXT NOT NULL,
                level TEXT NOT NULL,
                module TEXT NOT NULL,
                query TEXT NOT NULL,
                generation TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )                   
        ''')


def log_generation(session_id, level, module, query, generation):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        timestamp = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO logs (session_id, level, module, query, generation, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)            
        ''', (session_id, level, module, query, generation, timestamp))


def get_session_logs(session_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM logs WHERE session_id = ? ORDER BY timestamp DESC',
            (session_id,)
        )
        return cursor.fetchall()


def get_logs():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM logs ORDER BY timestamp DESC'
        )
        return cursor.fetchall()


setup_database()