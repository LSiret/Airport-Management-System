# Import necessary files
from AirportController import AirportController
from flask import Flask, render_template, request, redirect, url_for, flash

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = 'bigSecret123'

# Define a route for the home page
@app.route('/')
def home():

    # Get carbon logs
    logs = airport_controller.get_carbon_logs()

    return render_template('index.html', logs=logs)

@app.route('/flights')
def flights():
    return render_template('flights.html', flights=airport_controller.flights)

@app.post('/add_flight')
def add_flight():
    data = request.form
    airport_controller.add_flight(
        data['flight_id'], data['departure_airport'], data['arrival_airport'],
        data['departure_time'], data['arrival_time']
    )
    return redirect(url_for('flights'))

@app.post('/update_flight_status')
def update_flight_status():
    flight_id = request.form['flight_id']
    status = request.form['status']
    airport_controller.update_flight_status(flight_id, status)
    return redirect(url_for('flights'))

@app.post('/remove_flight')
def remove_flight():
    flight_id = request.form['flight_id']
    airport_controller.remove_flight(flight_id)
    return redirect(url_for('flights'))

@app.route('/checkin')
def checkin():
    return render_template('checkin.html', flights=airport_controller.flights)

@app.post('/checkin_passenger')
def checkin_passenger():
    flight_id = request.form['flight_id']
    passenger_id = request.form['passenger_id']
    passenger_name = request.form['passenger_name']
    luggage = request.form.get('luggage')
    seat = request.form.get('seat')

    try:
        airport_controller.add_passenger(flight_id, passenger_id, passenger_name, luggage, seat)
        flash(f"Passenger {passenger_name} successfully checked in for flight {flight_id}.", 'success')
    except Exception as e:
        flash(f"Check-in failed: {str(e)}", 'danger')

    return redirect(url_for('checkin'))

@app.route('/analytics')
def analytics():
    delay_info = airport_controller.get_delay_summary()
    carbon_avg = airport_controller.get_avg_carbon_emission()
    passenger_stats = airport_controller.get_passenger_stats()

    return render_template('analytics.html',
                           delays=delay_info,
                           carbon_avg=carbon_avg,
                           passenger_stats=passenger_stats)

@app.route('/emissions')
def emissions():
    return render_template('emissions.html', flights=airport_controller.flights)

@app.post('/log_emissions')
def log_emissions():
    flight_id = request.form['flight_id']
    source = request.form['source']
    carbon_output = request.form['carbon_output']

    try:
        airport_controller.log_emission(flight_id, source, carbon_output)
        flash(f"Emission logged for flight {flight_id}.", 'success')
    except Exception as e:
        flash(f"Logging failed: {str(e)}", 'danger')

    return redirect(url_for('emissions'))



# Check this file was run directly
if __name__ == '__main__':
    
    # Initialize the AirportController
    airport_controller = AirportController()

    # Run the Flask app
    app.run(debug=True)

