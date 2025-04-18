import sqlite3

class CarbonLog:
    """
    This class is used to log carbon emissions data to a table using SQLite.
    """

    def __init__(self):

        # Initialize database connection
        self.conn = sqlite3.connect('.db/carbon_log.db')
        self.cursor = self.conn.cursor()

        # Create table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS carbon_log (
                id INTEGER PRIMARY KEY,
                flight_id TEXT NOT NULL,
                source TEXT,
                carbon_output REAL
            )
        ''')
        self.conn.commit()

    # Log new data
    def log_emission(self, flight_id, source, carbon_output):

        # Insert new emission data
        self.cursor.execute('''
            INSERT INTO carbon_log (flight_id, source, carbon_output)
            VALUES (?, ?, ?)
        ''', (flight_id, source, carbon_output))
        self.conn.commit()
    
    # Show all logged data
    def show_data_all(self):

        # Fetch all data from the table
        self.cursor.execute('''
            SELECT * FROM carbon_log
        ''')
        rows = self.cursor.fetchall()

        print(f"Showing all emissions data:")

        # Print the data
        for row in rows:
            print(row)
    
    # Show data for a specific flight
    def show_data_flight(self, flight_id):

        # Fetch data for the specific flight
        self.cursor.execute('''
            SELECT * FROM carbon_log WHERE flight_id = ?
        ''', (flight_id,))
        rows = self.cursor.fetchall()

        print(f"Showing emissions data for flight {flight_id}:")

        # Print the data
        for row in rows:
            print(row)
    
    def __del__(self):

        # Close the database connection
        self.conn.close()
        
