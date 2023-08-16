import os
import sqlite3
from datetime import datetime

DB_NAME = 'logs.db'
DB_PATH = os.path.join('db', DB_NAME)


def setup_database():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Create a generation log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS generation_logs (
                id INTEGER PRIMARY KEY,
                session_id TEXT NOT NULL,
                query TEXT NOT NULL,
                generation TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )                   
        ''')

        # Create a classification log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS classification_logs (
                id INTEGER PRIMARY KEY,
                session_id TEXT NOT NULL,
                history TEXT NOT NULL,
                response TEXt NOT NULL,
                classification TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )                   
        ''')


def log_generation(session_id: str, query, generation: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        timestamp = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO generation_logs (session_id, query, generation, timestamp)
            VALUES (?, ?, ?, ?)            
        ''', (session_id, query, generation, timestamp))


def log_classification(session_id: str, history: str, response: str, classification: bool):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        timestamp = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO classification_logs (session_id, history, response, 
            classification, timestamp) VALUES (?, ?, ?, ?, ?)
        ''', (session_id, history, response, classification, timestamp))


def get_session_generation_logs(session_id: str) -> list:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        # Get generation logs for the session
        cursor.execute(
            'SELECT * FROM generation_logs WHERE session_id = ? '
            'ORDER BY timestamp DESC',
            (session_id,)
        )

        return cursor.fetchall()


def get_session_classification_logs(session_id: str) -> list:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        # Get classification logs for the session
        cursor.execute(
            'SELECT * FROM classification_logs WHERE session_id = ? '
            'ORDER BY timestamp DESC',
            (session_id,)
        )

        return cursor.fetchall()


setup_database()