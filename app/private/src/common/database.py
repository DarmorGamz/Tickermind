import sqlite3
from contextlib import contextmanager
from typing import List, Tuple, Any

class Database:
    """Singleton class for managing SQLite database connections and queries."""
    _instance = None

    def __new__(cls, db_path: str, primary_table: str, secondary_table: str, foreign_key: str):
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
            cls._instance.foreign_key = foreign_key
            cls._instance._create_connection()
            cls._instance._ensure_tables()
        return cls._instance

    def _create_connection(self):
        """Initializes the SQLite database connection with row factory."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

    def _ensure_tables(self):
        """Ensures primary and secondary tables exist with auto-incrementing IDs."""
        with self._get_cursor() as cursor:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.primary_table} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticker TEXT NOT NULL UNIQUE
                )
            """)
            cursor.execute(f"""
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

    @contextmanager
    def _get_cursor(self):
        """Context manager for handling database cursor operations."""
        cursor = self.conn.cursor()
        try:
            yield cursor
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def execute(self, query: str, params: Tuple = ()) -> None:
        """Executes a SQL query with optional parameters.

        Args:
            query (str): SQL query with {primary_table} or {secondary_table} placeholders.
            params (Tuple, optional): Parameters for the SQL query.
        """
        query = query.replace("{primary_table}", self.primary_table).replace("{secondary_table}", self.secondary_table)
        with self._get_cursor() as cursor:
            cursor.execute(query, params)

    def fetch_one(self, query: str, params: Tuple = ()) -> dict:
        """Fetches a single row from the database as a dictionary.

        Args:
            query (str): SQL query with {primary_table} or {secondary_table} placeholders.
            params (Tuple, optional): Parameters for the SQL query.

        Returns:
            dict: A dictionary representing the fetched row, or None if no results.
        """
        query = query.replace("{primary_table}", self.primary_table).replace("{secondary_table}", self.secondary_table)
        with self._get_cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchone()
            return dict(result) if result else None

    def fetch_all(self, query: str, params: Tuple = ()) -> List[dict]:
        """Fetches all rows from the database as a list of dictionaries.

        Args:
            query (str): SQL query with {primary_table} or {secondary_table} placeholders.
            params (Tuple, optional): Parameters for the SQL query.

        Returns:
            List[dict]: A list of dictionaries representing the fetched rows.
        """
        query = query.replace("{primary_table}", self.primary_table).replace("{secondary_table}", self.secondary_table)
        with self._get_cursor() as cursor:
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def fetch_by_reference(self, primary_id: Any) -> List[dict]:
        """Fetches rows from the secondary table referencing a specific primary table ID.

        Args:
            primary_id (Any): The ID from the primary table to match against the foreign key.

        Returns:
            List[dict]: List of dictionaries for rows in the secondary table.
        """
        query = f"SELECT * FROM {self.secondary_table} WHERE {self.foreign_key} = ?"
        return self.fetch_all(query, (primary_id,))

    def fetch_joined(self, primary_id: Any) -> List[dict]:
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
        return self.fetch_all(query, (primary_id,))

    def close(self):
        """Closes the database connection and resets the singleton instance."""
        self.conn.close()
        Database._instance = None


'''
# Initialize Database singleton
db = Database("mydb.db", primary_table="users", secondary_table="orders", foreign_key="user_id")

# Add a user (primary table)
db.execute("INSERT INTO {primary_table} (name) VALUES (?)", ("Alice",))

# Add an order (secondary table) referencing user ID 1
db.execute("INSERT INTO {secondary_table} ({foreign_key}, item) VALUES (?, ?)", (1, "book"))

# Get a single user by ID
user = db.fetch_one("SELECT * FROM {primary_table} WHERE id = ?", (1,))
print(user)  # {'id': 1, 'name': 'Alice'}

# Get all orders for user ID 1
orders = db.fetch_by_reference(1)
print(orders)  # [{'id': 1, 'user_id': 1, 'item': 'book'}]

# Get joined user and order data for user ID 1
joined = db.fetch_joined(1)
print(joined)  # [{'id': 1, 'name': 'Alice', 'id': 1, 'user_id': 1, 'item': 'book'}]

# Update user name
db.execute("UPDATE {primary_table} SET name = ? WHERE id = ?", ("Bob", 1))

# Delete an order
db.execute("DELETE FROM {secondary_table} WHERE id = ?", (1,))

# Close database
db.close()
'''