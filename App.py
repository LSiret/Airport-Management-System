# Import necessary files
from AirportController import AirportController

# Initialize the AirportController
airport_controller = AirportController()

# Add flights to the airport controller
airport_controller.add_flight(flight_id="FL123", departure_airport="AP001", arrival_airport="AP002", departure_time="12:00", arrival_time="16:00", status='On Time')
airport_controller.add_flight(flight_id="FL456", departure_airport="AP002", arrival_airport="AP001", departure_time="16:00", arrival_time="20:00", status='Delayed')

# Add passengers to the flight
airport_controller.add_passenger(flight_id="FL123", passenger_id="P001", passenger_name="John Doe")
airport_controller.add_passenger(flight_id="FL456", passenger_id="P002", passenger_name="Jane Smith")

# Log emissions for the flight
airport_controller.log_emission("FL123", "Fuel Consumption", 1000)
airport_controller.log_emission("FL456", "Fuel Consumption", 2000)
airport_controller.log_emission("FL123", "Flight Operations", 500)
airport_controller.log_emission("FL456", "Flight Operations", 750)

# Show carbon logs for the flight
airport_controller.show_carbon_logs("FL123")
airport_controller.show_carbon_logs()
