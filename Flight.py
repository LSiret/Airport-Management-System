import sqlite3
from Passenger import Passenger

class Flight:
    def __init__(self, flight_id, departure_airport=None, arrival_airport=None,
                 departure_time=None, arrival_time=None, status=None, passengers=None):
        
        self.conn = sqlite3.connect('.db/flights.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.flight_id = flight_id

        # Create tables if not exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS flights (
                flight_id TEXT PRIMARY KEY,
                departure_airport TEXT,
                arrival_airport TEXT,
                departure_time TEXT,
                arrival_time TEXT,
                status TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS passengers (
                passenger_id TEXT,
                name TEXT,
                flight_id TEXT,
                luggage_id TEXT,
                seat TEXT,
                PRIMARY KEY (passenger_id, flight_id),
                FOREIGN KEY (flight_id) REFERENCES flights(flight_id)
            )
        ''')

        # Check if flight exists
        self.cursor.execute("SELECT * FROM flights WHERE flight_id = ?", (flight_id,))
        flight_data = self.cursor.fetchone()

        if flight_data:
            # Load existing data
            _, self.departure_airport, self.arrival_airport, self.departure_time, self.arrival_time, self.status = flight_data
            self.passengers = self.list_passengers()
        else:
            # Create new flight record
            self.departure_airport = departure_airport
            self.arrival_airport = arrival_airport
            self.departure_time = departure_time
            self.arrival_time = arrival_time
            self.status = status
            self.passengers = passengers if passengers is not None else []

            self.cursor.execute('''
                INSERT INTO flights (flight_id, departure_airport, arrival_airport, departure_time, arrival_time, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (flight_id, departure_airport, arrival_airport, departure_time, arrival_time, status))
            self.conn.commit()

    def __str__(self):
        return f"Flight {self.flight_id} from {self.departure_airport} to {self.arrival_airport} departing at {self.departure_time} and arriving at {self.arrival_time}"

    def update_status(self, status):
        self.status = status
        self.cursor.execute("UPDATE flights SET status = ? WHERE flight_id = ?", (status, self.flight_id))
        self.conn.commit()

    def add_passenger(self, passenger: Passenger):
        self.cursor.execute('''
            SELECT * FROM passengers WHERE passenger_id = ? AND flight_id = ?
        ''', (passenger.passenger_id, self.flight_id))
        if self.cursor.fetchone():
            print(f"Passenger {passenger.passenger_id} is already on flight {self.flight_id}.")
            return

        self.cursor.execute('''
            INSERT INTO passengers (passenger_id, name, flight_id)
            VALUES (?, ?, ?)
        ''', (passenger.passenger_id, passenger.name, self.flight_id))
        self.conn.commit()
        print(f"Passenger {passenger.passenger_id} added to flight {self.flight_id}.")

    def remove_passenger(self, passenger_id):
        self.cursor.execute('''
            DELETE FROM passengers WHERE passenger_id = ? AND flight_id = ?
        ''', (passenger_id, self.flight_id))
        if self.cursor.rowcount == 0:
            print(f"Passenger {passenger_id} not found on flight {self.flight_id}.")
        else:
            self.conn.commit()
            print(f"Passenger {passenger_id} removed from flight {self.flight_id}.")

    def list_passengers(self):
        self.cursor.execute('''
            SELECT passenger_id, name FROM passengers WHERE flight_id = ?
        ''', (self.flight_id,))
        return self.cursor.fetchall()
