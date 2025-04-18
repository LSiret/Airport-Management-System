class Passenger:
    """
    Class representing a passenger in an airline system.
    Attributes:
        name (str): Name of the passenger.
        passenger_id (int): Unique ID for the passenger.
        luggage (int): ID of the luggage associated with the passenger.
        seat_number (str): Seat number assigned to the passenger.
    """
    
    # Constructor to initialize passenger details
    def __init__(self, name: str, passenger_id: int, luggageID: int=None, seat_number: int=None):
        self.name = name
        self.passenger_id = passenger_id
        self.luggage = luggageID
        self.seat_number = None

    def __str__(self):
        return f"Passenger {self.name}, Luggage: {self.luggage}, Seat Number: {self.seat_number}"

    def checkIn(self, seat_number: str):
        
        # Logic to check in the passenger
        self.seat_number = seat_number

        # Log to show completion of check-in
        print(f"Passenger {self.name} has checked in.")