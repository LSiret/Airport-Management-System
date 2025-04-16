import Flight
import Passenger

class AirportController:
    def __init__(self, flights=[]):
        self.flights = flights

    def get_flight_by_id(self, flight_id):

        # Check if the flight exists
        for flight in self.flights:
            if flight.flight_number == flight_id:
                return flight
            else:
                print(f"Flight {flight_id} not found.")
                return None

    def update_flight_status(self, flight_id, status):
        
        # Get the flight
        flight = self.get_flight_by_id(flight_id)
        
        # Check if flight was found
        if flight:
            flight.status = status
            print(f"Flight {flight_id} status updated to {status}.")

    def add_flight(self, flight):

        # Add the flight to the list
        self.flights.append(flight)
        print(f"Flight {flight.flight_number} added.")

    def remove_flight(self, flight_id):

        # Get the flight
        flight = self.get_flight_by_id(flight_id)
        
        # Check if flight was found
        if flight:
            self.flights.remove(flight)
            print(f"Flight {flight_id} removed.")
