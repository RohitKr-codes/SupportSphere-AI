import sqlite3

from src.config import Config


class FeedbackManager:

    def __init__(self):

        self.conn = sqlite3.connect(
            Config.DB_PATH,
            check_same_thread=False
        )

        self.create_table()

    def create_table(self):

        cursor = self.conn.cursor()

        cursor.execute("""

        CREATE TABLE IF NOT EXISTS feedback(

            id INTEGER PRIMARY KEY,

            rating INTEGER,

            comments TEXT,

            created_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP

        )

        """)

        self.conn.commit()

    def save_feedback(

        self,

        rating,

        comments

    ):

        cursor = self.conn.cursor()

        cursor.execute("""

        INSERT INTO feedback(

            rating,
            comments

        )

        VALUES (?,?)

        """,

        (

            rating,
            comments

        ))

        self.conn.commit()