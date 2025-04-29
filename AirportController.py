from Flight import Flight
from Passenger import Passenger
from CarbonLog import CarbonLog
from Luggage import Luggage
import sqlite3

class AirportController:
    def __init__(self):
        self.carbon_log = CarbonLog()
        self.flights = self.load_flights_from_db()

    def load_flights_from_db(self):
        conn = sqlite3.connect('.db/flights.db')
        cursor = conn.cursor()

        conn.execute('''
            CREATE TABLE IF NOT EXISTS flights (
                flight_id TEXT PRIMARY KEY,
                departure_airport TEXT,
                arrival_airport TEXT,
                departure_time TEXT,
                arrival_time TEXT,
                status TEXT
            )
        ''')

        cursor.execute("SELECT * FROM flights")
        flight_rows = cursor.fetchall()

        if not flight_rows:
            print("No flights found in the database.")
            return []

        flights = []
        for row in flight_rows:
            flight_id, departure_airport, arrival_airport, departure_time, arrival_time, status = row

            # Get passengers for this flight
            cursor.execute("SELECT * FROM passengers WHERE flight_id = ?", (flight_id,))
            passenger_rows = cursor.fetchall()
            print(passenger_rows)
            passengers = [
                Passenger(p_id, name, luggage, seat)
                for (p_id, name, luggage, seat, _) in passenger_rows
            ]

            flight = Flight(
                flight_id, departure_airport, arrival_airport,
                departure_time, arrival_time, status, passengers
            )
            flights.append(flight)

        conn.close()
        return flights

    def get_flight_by_id(self, flight_id: str):
        for flight in self.flights:
            if flight.flight_id == flight_id:
                return flight
        print(f"Flight {flight_id} not found.")
        return None

    def update_flight_status(self, flight_id: str, status: str):
        flight = self.get_flight_by_id(flight_id)
        if flight:
            flight.update_status(status)
            print(f"Flight {flight_id} status updated to {status}.")

    def add_flight(self, flight_id: str, departure_airport: str, arrival_airport: str, departure_time: str, arrival_time: str, status: str=None):
        for existing_flight in self.flights:
            if existing_flight.flight_id == flight_id:
                print(f"Flight {flight_id} already exists.")
                return
        flight = Flight(flight_id, departure_airport, arrival_airport, departure_time, arrival_time, status)
        self.flights.append(flight)
        print(f"Flight {flight.flight_id} added.")

    def remove_flight(self, flight_id: str):
        conn = sqlite3.connect("flights.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM flights WHERE flight_id = ?", (flight_id,))
        cursor.execute("DELETE FROM passengers WHERE flight_id = ?", (flight_id,))
        conn.commit()
        conn.close()
        self.flights = [f for f in self.flights if f.flight_id != flight_id]
        print(f"Flight {flight_id} removed.")

    def add_passenger(self, flight_id: str, passenger_id: str, passenger_name: str, luggage=None, seat=None):
        passenger = Passenger(passenger_id, passenger_name, luggage, seat)
        flight = self.get_flight_by_id(flight_id)
        if flight:
            flight.add_passenger(passenger)

    def remove_passenger(self, flight_id: str, passenger_id: str):
        flight = self.get_flight_by_id(flight_id)
        if flight:
            flight.remove_passenger(passenger_id)

    def verify_passenger(self, flight_id: str, passenger_id: str):
        flight = self.get_flight_by_id(flight_id)
        if flight:
            for passenger in flight.passengers:
                if passenger.passenger_id == passenger_id:
                    print(f"Passenger {passenger_id} verified on flight {flight_id}.")
                    return True
            print(f"Passenger {passenger_id} not found on flight {flight_id}.")
        return False
    
    def log_new_luggage(self, luggage_id: str, weight: float, flight_id: str, passenger_id: str, status: str=None):
        
        # Check if flight exists
        flight = self.get_flight_by_id(flight_id)
        if not flight:
            print(f"Flight {flight_id} not found. Cannot add luggage.")
            return

        # Check if passenger exists
        passenger = next((p for p in flight.passengers if p.passenger_id == passenger_id), None)
        if not passenger:
            print(f"Passenger {passenger_id} not found on flight {flight_id}. Cannot add luggage.")
            return
        
        # Check if luggage already exists
        if any(l.luggage_id == luggage_id for l in passenger.luggage):
            print(f"Luggage {luggage_id} already exists for passenger {passenger_id}.")
            return
        
        # Create and add luggage
        luggage = Luggage(luggage_id, weight, flight_id, passenger_id, status)
        passenger.add_luggage(luggage)
        print(f"Luggage {luggage_id} added to flight {flight_id} for passenger {passenger_id}.")
    
    def update_luggage_status(self, luggage_id: str, status: str):
        conn = sqlite3.connect('.db/luggage.db')
        cursor = conn.cursor()

        # Update luggage status
        cursor.execute('''
            UPDATE luggage
            SET status = ?
            WHERE luggage_id = ?
        ''', (status, luggage_id))
        conn.commit()

        # Log the status update in history
        cursor.execute('''
            INSERT INTO luggage_history (luggage_id, status)
            VALUES (?, ?)
        ''', (luggage_id, status))
        conn.commit()
        conn.close()
        
        print(f"Luggage {luggage_id} status updated to {status}.")


    def get_carbon_logs(self, flight_id: str=None):
        if flight_id:
            return self.carbon_log.get_data_flight(flight_id)
        else:
            return self.carbon_log.get_data_all()

    def log_emission(self, flight_id: str, source: str, carbon_output: str):
        flight = self.get_flight_by_id(flight_id)
        if flight:
            self.carbon_log.log_emission(flight_id, source, carbon_output)
            print(f"Emission logged for flight {flight_id} from {source} with output {carbon_output}.")

    def get_delay_summary(self):
        return [f for f in self.flights if f.status and "delay" in f.status.lower()]

    def get_passenger_stats(self):
        stats = []
        for flight in self.flights:
            count = len(flight.passengers)
            stats.append((flight.flight_id, count))

        if stats:
            values = [c for _, c in stats]
            return {
                "stats": stats,
                "max": max(stats, key=lambda x: x[1]),
                "min": min(stats, key=lambda x: x[1]),
                "avg": round(sum(values) / len(values), 2)
            }
        else:
            return {"stats": [], "max": None, "min": None, "avg": 0}

    def get_avg_carbon_emission(self):
        logs = self.carbon_log.get_data_all()
        if not logs:
            return 0
        total = sum(row[3] for row in logs)  # assuming carbon_output is at index 3
        return round(total / len(logs), 2)
