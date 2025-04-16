class Passenger:
    
    # Constructor to initialize passenger details
    def __init__(self, name: str, passengerID: int, luggageID: int, flight):
        self.name = name
        self.passengerID = passengerID
        self.luggage = luggageID
        self.seat_number = None

    def __str__(self):
        return f"Passenger {self.name}, Age: {self.age}, Luggage: {self.luggage}, Seat Number: {self.seat_number}"

    def checkIn(self):
        
        # Logic to check in the passenger

        # Log to show completion of check-in
        print(f"Passenger {self.name} has checked in.")