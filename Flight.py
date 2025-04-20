from Passenger import Passenger

class Flight:

    """
    Class to represent a flight with its details and passengers.
    """

    # Constructor to initialize flight details
    def __init__(self, flight_id, departure_airport, arrival_airport, departure_time, arrival_time, status=None, passengers=[]):
        self.flight_id = flight_id
        self.departure_airport = departure_airport
        self.arrival_airport = arrival_airport
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.status = status
        self.passengers = passengers

    def __str__(self):
        return f"Flight {self.flight_id} from {self.departure_airport} to {self.arrival_airport} departing at {self.departure_time} and arriving at {self.arrival_time}"
    
    def update_status(self, status):
        self.status = status

    def add_passenger(self, passenger : Passenger):
        # Check if the passenger is already on the flight
        for existing_passenger in self.passengers:
            if existing_passenger.passenger_id == passenger.passenger_id:
                print(f"Passenger {passenger.passenger_id} is already on flight {self.flight_id}.")
                return
        self.passengers.append(passenger)
        print(f"Passenger {passenger.passenger_id} added to flight {self.flight_id}.")
    
    def remove_passenger(self, passenger_id):
        
        # Check if the passenger exists
        for passenger in self.passengers:
            if passenger.passenger_id == passenger_id:
                self.passengers.remove(passenger)
                print(f"Passenger {passenger_id} removed from flight {self.flight_id}.")
                return
        print(f"Passenger {passenger_id} not found on flight {self.flight_id}.")

