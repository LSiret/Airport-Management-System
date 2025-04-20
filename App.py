# Import necessary files
from AirportController import AirportController
from flask import Flask, render_template

# Initialize the Flask app
app = Flask(__name__)

# Define a route for the home page
@app.route('/')
def home():

    # Get carbon logs
    logs = airport_controller.get_carbon_logs()

    return render_template('index.html', logs=logs)

# Check this file was run directly
if __name__ == '__main__':
    
    # Initialize the AirportController
    airport_controller = AirportController()

    # Run the Flask app
    app.run(debug=True)

