from Flight import Flight
from Passenger import Passenger

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

    def verify_passenger(self, flight_id, passenger_id):

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
    
    def show_carbon_logs(self, flight_id=None):
        
        # Display Logs
        if flight_id:
            print(f"Showing logs for flight {flight_id}:")
        else:
            print("Showing all logs:")


