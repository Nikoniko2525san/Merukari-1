import sqlite3
from pathlib import Path

DB_PATH = Path("data/merukari.db")


class Database:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.db_path)
        self._create_tables()

    def _create_tables(self) -> None:
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS listings (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                purchase_price INTEGER NOT NULL,
                expected_sale_price INTEGER NOT NULL,
                url TEXT,
                notified INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        self.connection.commit()

    def is_notified(self, listing_id: str) -> bool:
        cursor = self.connection.execute(
            """
            SELECT notified
            FROM listings
            WHERE id = ?
            """,
            (listing_id,),
        )

        row = cursor.fetchone()

        if row is None:
            return False

        return bool(row[0])

    def add_listing(
        self,
        listing_id: str,
        title: str,
        purchase_price: int,
        expected_sale_price: int,
        url: str = "",
    ) -> None:
        self.connection.execute(
            """
            INSERT INTO listings
            (
                id,
                title,
                purchase_price,
                expected_sale_price,
                url
            )
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                title = excluded.title,
                purchase_price = excluded.purchase_price,
                expected_sale_price = excluded.expected_sale_price,
                url = excluded.url
            """,
            (
                listing_id,
                title,
                purchase_price,
                expected_sale_price,
                url,
            ),
        )

        self.connection.commit()

    def mark_notified(self, listing_id: str) -> None:
        self.connection.execute(
            """
            UPDATE listings
            SET notified = 1
            WHERE id = ?
            """,
            (listing_id,),
        )

        self.connection.commit()

    def close(self) -> None:
        self.connection.close()
