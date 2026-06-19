import sqlite3

from src.config import Config


class Analytics:

    def __init__(self):

        self.conn = sqlite3.connect(
            Config.DB_PATH,
            check_same_thread=False
        )

        self.create_table()

    def create_table(self):

        cursor = self.conn.cursor()

        cursor.execute("""

        CREATE TABLE IF NOT EXISTS analytics(

            id INTEGER PRIMARY KEY,

            persona TEXT,

            query TEXT,

            escalated INTEGER,

            created_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP

        )

        """)

        self.conn.commit()

    def log_query(

        self,

        persona,

        query,

        escalated

    ):

        cursor = self.conn.cursor()

        cursor.execute("""

        INSERT INTO analytics(

            persona,
            query,
            escalated

        )

        VALUES(?,?,?)

        """,

        (

            persona,
            query,
            int(escalated)

        ))

        self.conn.commit()