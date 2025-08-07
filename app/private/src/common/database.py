import aiosqlite
from contextlib import asynccontextmanager
from typing import List, Tuple, Any
import os
import aiofiles

class Database:
    """Singleton class for managing async SQLite database connections and queries."""
    _instance = None

    def __new__(cls, db_path: str= "", primary_table: str= "", secondary_table: str= "", news_table: str = "news_table", foreign_key: str= "stock_id"):
        """Ensures a single instance of the Database class.

        Args:
            db_path (str): Path to the SQLite database file.
            primary_table (str): Name of the primary table (referenced by foreign key).
            secondary_table (str): Name of the secondary table (contains foreign key).
            foreign_key (str): Name of the foreign key column in the secondary table.

        Returns:
            Database: Singleton instance of the Database class.
        """
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.db_path = db_path
            cls._instance.primary_table = primary_table
            cls._instance.secondary_table = secondary_table
            cls._instance.news_table = news_table
            cls._instance.foreign_key = foreign_key
            cls._instance.loop = None
            cls._instance.conn = None
        return cls._instance

    async def _create_connection(self):
        """Initializes the async SQLite database connection with row factory."""
        if self.conn is None:
            self.conn = await aiosqlite.connect(self.db_path)
            self.conn.row_factory = aiosqlite.Row
            await self._ensure_tables()

    async def _ensure_tables(self):
        """Ensures primary and secondary tables exist with auto-incrementing IDs."""
        async with self._get_cursor() as cursor:
            await cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.primary_table} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticker TEXT NOT NULL UNIQUE
                )
            """)
            await cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.secondary_table} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    {self.foreign_key} INTEGER,
                    date TEXT NOT NULL,
                    close REAL NOT NULL,
                    volume INTEGER NOT NULL,
                    FOREIGN KEY ({self.foreign_key}) REFERENCES {self.primary_table}(id),
                    UNIQUE ({self.foreign_key}, date)
                )
            """)
            await cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.news_table} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    {self.foreign_key} INTEGER,
                    date TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    content TEXT,
                    source TEXT NOT NULL,
                    sentiment_label TEXT,
                    FOREIGN KEY ({self.foreign_key}) REFERENCES {self.primary_table}(id),
                    UNIQUE ({self.foreign_key}, date, description)
                )
            """)
            await self.conn.commit()

    @asynccontextmanager
    async def _get_cursor(self):
        """Async context manager for handling database cursor operations."""
        if self.conn is None:
            await self._create_connection()
        cursor = await self.conn.cursor()
        try:
            yield cursor
            await self.conn.commit()
        except Exception as e:
            await self.conn.rollback()
            raise e
        finally:
            await cursor.close()

    async def execute(self, query: str, params: Tuple = ()) -> None:
        """Executes an async SQL query with optional parameters.

        Args:
            query (str): SQL query with {primary_table}, {secondary_table}, or {foreign_key} placeholders.
            params (Tuple, optional): Parameters for the SQL query.
        """
        query = (
            query.replace("{primary_table}", self.primary_table)
            .replace("{secondary_table}", self.secondary_table)
            .replace("{foreign_key}", self.foreign_key)
            .replace("{news_table}", self.news_table)
        )

        os.makedirs('/data', exist_ok=True)
        async with aiofiles.open('/data/execute.txt', 'a') as f:
            await f.write(f"query: {query}\n")
            await f.write(f"params: {params}\n")

        async with self._get_cursor() as cursor:
            await cursor.execute(query, params)

    async def fetch_one(self, query: str, params: Tuple = ()) -> dict:
        """Fetches a single row from the database as a dictionary.

        Args:
            query (str): SQL query with {primary_table}, {secondary_table}, or {foreign_key} placeholders.
            params (Tuple, optional): Parameters for the SQL query.

        Returns:
            dict: A dictionary representing the fetched row, or None if no results.
        """
        query = (
            query.replace("{primary_table}", self.primary_table)
            .replace("{secondary_table}", self.secondary_table)
            .replace("{foreign_key}", self.foreign_key)
            .replace("{news_table}", self.news_table)
        )

        os.makedirs('/data', exist_ok=True)
        async with aiofiles.open('/data/query.txt', 'a') as f:
            await f.write(f"query: {query}\n")
            await f.write(f"params: {params}\n")

        async with self._get_cursor() as cursor:
            await cursor.execute(query, params)
            result = await cursor.fetchone()
            return dict(result) if result else None

    async def fetch_all(self, query: str, params: Tuple = ()) -> List[dict]:
        """Fetches all rows from the database as a list of dictionaries.

        Args:
            query (str): SQL query with {primary_table} or {secondary_table} placeholders.
            params (Tuple, optional): Parameters for the SQL query.

        Returns:
            List[dict]: A list of dictionaries representing the fetched rows.
        """
        query = (
            query.replace("{primary_table}", self.primary_table)
            .replace("{secondary_table}", self.secondary_table)
            .replace("{foreign_key}", self.foreign_key)
            .replace("{news_table}", self.news_table)
        )
        async with self._get_cursor() as cursor:
            await cursor.execute(query, params)
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    async def fetch_by_reference(self, primary_id: Any) -> List[dict]:
        """Fetches rows from the secondary table referencing a specific primary table ID.

        Args:
            primary_id (Any): The ID from the primary table to match against the foreign key.

        Returns:
            List[dict]: List of dictionaries for rows in the secondary table.
        """
        query = f"SELECT * FROM {self.secondary_table} WHERE {self.foreign_key} = ?"
        return await self.fetch_all(query, (primary_id,))

    async def fetch_joined(self, primary_id: Any) -> List[dict]:
        """Fetches rows from both tables joined on the foreign key for a specific primary ID.

        Args:
            primary_id (Any): The ID from the primary table to match.

        Returns:
            List[dict]: List of dictionaries with columns from both tables.
        """
        query = f"""
            SELECT * FROM {self.primary_table} p
            JOIN {self.secondary_table} s ON p.id = s.{self.foreign_key}
            WHERE p.id = ?
        """
        return await self.fetch_all(query, (primary_id,))

    async def close(self):
        """Closes the database connection and resets the singleton instance."""
        if self.conn is not None:
            await self.conn.close()
            self.conn = None
            Database._instance = None