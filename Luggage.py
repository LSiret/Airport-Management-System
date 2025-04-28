import sqlite3

class Luggage:

    """
    An instance of this class represents a luggage item with its assiciated properties.
    """

    def __init__(self, luggage_id: str, weight: float, flight_id: str, passenger_id: str, status: str = None):
        """
        Initializes a luggage item with its ID, weight, associated flight ID, and passenger ID.
        
        :param luggage_id: Unique identifier for the luggage item.
        :param weight: Weight of the luggage in kilograms.
        :param flight_id: ID of the flight associated with this luggage.
        :param passenger_id: ID of the passenger associated with this luggage.
        """
        self.luggage_id = luggage_id
        self.weight = weight
        self.flight_id = flight_id
        self.passenger_id = passenger_id
        self.status = status

        # Create table if it doesn't exist
        self.conn = sqlite3.connect('.db/luggage.db', check_same_thread=False)
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS luggage (
                    luggage_id TEXT PRIMARY KEY,
                    weight REAL,
                    flight_id TEXT,
                    passenger_id TEXT,
                    status TEXT
                )
            ''')

            # Create table for update history if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS luggage_history (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    luggage_id TEXT FOREIGN KEY,
                    status TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Insert luggage item if it doesn't already exist
            cursor.execute('''
                INSERT OR IGNORE INTO luggage (luggage_id, weight, flight_id, passenger_id, status)
                VALUES (?, ?, ?, ?, ?)
            ''', (self.luggage_id, self.weight, self.flight_id, self.passenger_id, self.status))

            # Insert initial status into history
            if self.status:
                cursor.execute('''
                    INSERT INTO luggage_history (luggage_id, status)
                    VALUES (?, ?)
                ''', (self.luggage_id, self.status))
            self.conn.commit()


    def update_status(self, status: str):
        """
        Updates the status of the luggage item.
        
        :param status: New status for the luggage item.
        """
        self.status = status

        # Update the status in the database
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE luggage
                SET status = ?
                WHERE luggage_id = ?
            ''', (status, self.luggage_id))

            # Insert the new status into the history
            cursor.execute('''
                INSERT INTO luggage_history (luggage_id, status)
                VALUES (?, ?)
            ''', (self.luggage_id, status))

            # Commit the changes
            self.conn.commit()


