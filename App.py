# Example of initializing the CarbonLog class
from CarbonLog import CarbonLog

# Replace 'FL123' with the actual flight ID you want to use
flight_log = CarbonLog(flight_id='FL123')

flight_log.log_emission(source='Flight', carbon_output=100.0)
flight_log.log_emission(source='Airport', carbon_output=50.0)

flight_log_2 = CarbonLog(flight_id='FL456')
flight_log_2.log_emission(source='Flight', carbon_output=200.0)
flight_log_2.log_emission(source='Airport', carbon_output=75.0)

# Show all logged data
flight_log.show_data()