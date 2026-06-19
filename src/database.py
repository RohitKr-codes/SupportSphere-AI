import sqlite3
from pathlib import Path

from src.config import Config


class DatabaseManager:

    def __init__(self):

        Path("database").mkdir(
            exist_ok=True
        )

        self.conn = sqlite3.connect(
            Config.DB_PATH,
            check_same_thread=False
        )

        self.cursor = self.conn.cursor()

        self.create_tables()

    def create_tables(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            session_id TEXT,

            persona TEXT,

            user_message TEXT,

            bot_response TEXT,

            confidence REAL,

            escalated INTEGER,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            session_id TEXT,

            rating INTEGER,

            comments TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS escalations (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            session_id TEXT,

            persona TEXT,

            issue_summary TEXT,

            recommendation TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.conn.commit()

    def save_conversation(
        self,
        session_id,
        persona,
        user_message,
        bot_response,
        confidence,
        escalated
    ):

        self.cursor.execute("""
        INSERT INTO conversations (

            session_id,
            persona,
            user_message,
            bot_response,
            confidence,
            escalated

        )

        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            session_id,
            persona,
            user_message,
            bot_response,
            confidence,
            escalated
        ))

        self.conn.commit()

    def save_feedback(
        self,
        session_id,
        rating,
        comments
    ):

        self.cursor.execute("""
        INSERT INTO feedback (

            session_id,
            rating,
            comments

        )

        VALUES (?, ?, ?)
        """,
        (
            session_id,
            rating,
            comments
        ))

        self.conn.commit()

    def get_conversation_history(
        self,
        session_id
    ):

        self.cursor.execute("""
        SELECT
            user_message,
            bot_response
        FROM conversations
        WHERE session_id=?
        ORDER BY id ASC
        """,
        (session_id,)
        )

        return self.cursor.fetchall()