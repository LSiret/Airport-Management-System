class Flight:

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
        return f"Flight {self.flight_number} from {self.departure_airport} to {self.arrival_airport} departing at {self.departure_time} and arriving at {self.arrival_time}"
    
    def update_status(self, status):
        self.status = status
        print(f"Flight {self.flight_number} status updated to {status}.")

    def add_passenger(self, passenger):
        self.passengers.append(passenger)
        print(f"Passenger {passenger.name} added to flight {self.flight_number}.")