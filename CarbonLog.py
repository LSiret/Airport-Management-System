import sqlite3

class CarbonLog:

    def __init__(self, flight_id):
        self.flight_id = flight_id

        # Initialize database connection
        self.conn = sqlite3.connect('.db/carbon_log.db')
        self.cursor = self.conn.cursor()

        # Create table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS carbon_log (
                id INTEGER PRIMARY KEY,
                flight_id TEXT,
                source TEXT,
                carbon_output REAL
            )
        ''')
        self.conn.commit()

    # Log new data
    def log_emission(self, source, carbon_output):

        # Insert new emission data
        self.cursor.execute('''
            INSERT INTO carbon_log (flight_id, source, carbon_output)
            VALUES (?, ?, ?)
        ''', (self.flight_id, source, carbon_output))
        self.conn.commit()

        print(f"Emission logged for flight {self.flight_id} from {source} with output {carbon_output}.")
    
    # Show all logged data
    def show_data(self):

        # Fetch all data from the table
        self.cursor.execute('''
            SELECT * FROM carbon_log
        ''')
        rows = self.cursor.fetchall()

        print(f"All logged data for flight {self.flight_id}:")

        # Print the data
        for row in rows:
            print(row)
    
    def __del__(self):

        # Close the database connection
        self.conn.close()
        
