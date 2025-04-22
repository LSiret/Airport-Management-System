# Import necessary files
from AirportController import AirportController
from flask import Flask, render_template, request, redirect, url_for

# Initialize the Flask app
app = Flask(__name__)

# Define a route for the home page
@app.route('/')
def home():

    # Get carbon logs
    logs = airport_controller.get_carbon_logs()

    return render_template('index.html', logs=logs)

@app.route('/flights')
def flights():
    return render_template('flights.html', flights=airport_controller.flights)

@app.route('/add_flight', methods=['POST'])
def add_flight():
    data = request.form
    airport_controller.add_flight(
        data['flight_id'], data['departure_airport'], data['arrival_airport'],
        data['departure_time'], data['arrival_time']
    )
    return redirect(url_for('flights'))

@app.route('/update_flight_status', methods=['POST'])
def update_flight_status():
    flight_id = request.form['flight_id']
    status = request.form['status']
    airport_controller.update_flight_status(flight_id, status)
    return redirect(url_for('flights'))

@app.route('/remove_flight', methods=['POST'])
def remove_flight():
    flight_id = request.form['flight_id']
    airport_controller.remove_flight(flight_id)
    return redirect(url_for('flights'))


# Check this file was run directly
if __name__ == '__main__':
    
    # Initialize the AirportController
    airport_controller = AirportController()

    # Run the Flask app
    app.run(debug=True)

