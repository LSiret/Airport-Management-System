from Flight import Flight
from Passenger import Passenger
from CarbonLog import CarbonLog

class AirportController:
    def __init__(self, flights=[]):
        self.flights = flights
        self.carbon_log = CarbonLog()

    def get_flight_by_id(self, flight_id : str):

        # Check if the flight exists
        for flight in self.flights:
            if flight.flight_id == flight_id:
                return flight
        
        print(f"Flight {flight_id} not found.")
        return None

    def update_flight_status(self, flight_id: str, status: str):
        
        # Get the flight
        flight = self.get_flight_by_id(flight_id)
        
        # Check if flight was found
        if flight:
            flight.status = status
            print(f"Flight {flight_id} status updated to {status}.")

    def add_flight(self, flight_id: str, departure_airport: str, arrival_airport: str, departure_time: str, arrival_time: str, status: str=None):
        
        # Create a new flight
        flight = Flight(flight_id, departure_airport, arrival_airport, departure_time, arrival_time, status)

        # Check if flight already exists
        for existing_flight in self.flights:
            if existing_flight.flight_id == flight.flight_id:
                print(f"Flight {flight.flight_id} already exists.")
                return

        # Add the flight to the list
        self.flights.append(flight)
        print(f"Flight {flight.flight_id} added.")

    def remove_flight(self, flight_id: str):

        # Get the flight
        flight = self.get_flight_by_id(flight_id)
        
        # Check if flight was found
        if flight:
            self.flights.remove(flight)
            print(f"Flight {flight_id} removed.")

    def add_passenger(self, flight_id: str, passenger_id: str, passenger_name: str, luggage=None, seat=None):
        
        # Create a new passenger
        passenger = Passenger(passenger_id, passenger_name, luggage, seat)

        # Get the flight
        flight = self.get_flight_by_id(flight_id)

        # Check if flight was found
        if flight:
            flight.add_passenger(passenger)
    
    def remove_passenger(self, flight_id: str, passenger_id: str):

        # Get the flight
        flight = self.get_flight_by_id(flight_id)

        # Check if flight was found
        if flight:
            flight.remove_passenger(passenger_id)

    def verify_passenger(self, flight_id: str, passenger_id: str):

        flight = self.get_flight_by_id(flight_id)

        # Check if flight was found
        if flight:
            # Check if the passenger exists
            for passenger in flight.passengers:
                if passenger.passenger_id == passenger_id:
                    print(f"Passenger {passenger_id} verified on flight {flight_id}.")
                    return True
            print(f"Passenger {passenger_id} not found on flight {flight_id}.")
            return False
    
    def get_carbon_logs(self, flight_id: str=None):

        # Display Logs
        if flight_id:
            return self.carbon_log.get_data_flight(flight_id)
        else:
            return self.carbon_log.get_data_all()

    def log_emission(self, flight_id: str, source: str, carbon_output: str):

        # Get the flight
        flight = self.get_flight_by_id(flight_id)

        # Check if flight was found
        if flight:
            # Log the emission
            self.carbon_log.log_emission(flight_id, source, carbon_output)
            print(f"Emission logged for flight {flight_id} from {source} with output {carbon_output}.")



