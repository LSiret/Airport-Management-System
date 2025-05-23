# Import necessary files
from AirportController import AirportController
from flask import Flask, render_template, request, redirect, url_for, flash, session
from auth import register, login, log_event, load_users, save_users
import re
import random


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

# Add these new routes to App.py
@app.route('/security')
def security():
    if 'username' not in session:
        return redirect(url_for('security_login'))
    return render_template('security.html', username=session['username'], role=session.get('role'))

@app.route('/security/login', methods=['GET', 'POST'])
def security_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        success, message, role = login(username, password)
        
        if success:
            # Simulate 2FA (for demo purposes)
            session['2fa_pending'] = True
            session['2fa_code'] = str(random.randint(100000, 999999))
            session['temp_user'] = username
            session['temp_role'] = role
            flash(f"2FA code sent (simulated): {session['2fa_code']}", 'info')
            return redirect(url_for('security_2fa'))
        else:
            flash(message, 'danger')
    return render_template('security_login.html')

@app.route('/security/2fa', methods=['GET', 'POST'])
def security_2fa():
    if not session.get('2fa_pending'):
        return redirect(url_for('security_login'))
    
    if request.method == 'POST':
        user_code = request.form['code']
        if user_code == session.get('2fa_code'):
            session['username'] = session['temp_user']
            session['role'] = session['temp_role']
            session.pop('2fa_pending', None)
            log_event(f"{session['username']} logged in")
            flash("Login successful!", 'success')
            return redirect(url_for('security'))
        else:
            flash("Invalid 2FA code. Try again.", 'danger')
    return render_template('security_2fa.html', code=session.get('2fa_code'))


@app.route('/security/logout')
def security_logout():
    if 'username' in session:
        log_event(f"{session['username']} logged out")
        session.clear()
    return redirect(url_for('security_login'))

@app.route('/security/register', methods=['GET', 'POST'])
def security_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form.get('role', 'user')
        
        # Password validation
        if not (8 <= len(password) <= 10):
            flash("Password must be 8–10 characters long.", 'danger')
        elif not re.search(r"[A-Z]", password):
            flash("Password must include at least one uppercase letter.", 'danger')
        elif not re.search(r"[a-z]", password):
            flash("Password must include at least one lowercase letter.", 'danger')
        elif not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            flash("Password must include at least one special character.", 'danger')
        else:
            success, message = register(username, password, role)
            flash(message, 'success' if success else 'danger')
            if success:
                return redirect(url_for('security_login'))
    return render_template('security_register.html')

@app.route('/carbon-report')
def carbon_report():
    if 'username' not in session:
        return redirect(url_for('security_login'))
    users = load_users()
    username = session['username']
    footprint = users.get(username, {}).get('carbon_footprint', 0.0)
    return render_template('carbon_report.html', footprint=footprint)

@app.route('/update-info', methods=['GET', 'POST'])
def update_info():
    if 'username' not in session:
        return redirect(url_for('security_login'))

    users = load_users()
    username = session['username']

    if request.method == 'POST':
        users[username]['email'] = request.form['email']
        users[username]['phone'] = request.form['phone']
        save_users(users)
        flash("Information updated.", "success")
        return redirect(url_for('security'))

    user_data = users[username]
    return render_template('update_info.html', email=user_data.get('email', ''), phone=user_data.get('phone', ''))

@app.route('/add-travel', methods=['GET', 'POST'])
def add_travel():
    if 'username' not in session:
        return redirect(url_for('security_login'))

    users = load_users()
    username = session['username']

    if request.method == 'POST':
        try:
            distance = float(request.form['distance'])
            emissions = round(distance * 0.115, 2)
            users[username]['carbon_footprint'] += emissions
            save_users(users)
            flash(f"{emissions} kg CO₂ added to your footprint.", "success")
            return redirect(url_for('security'))
        except ValueError:
            flash("Please enter a valid distance.", "danger")

    return render_template('add_travel.html')

@app.route('/view-logs')
def view_logs():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('security_login'))

    try:
        with open('logs.txt', 'r') as f:
            logs = f.readlines()
    except FileNotFoundError:
        logs = ["No log file found."]

    return render_template('view_logs.html', logs=logs)

@app.route('/manage-users')
def manage_users():
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('security_login'))

    users = load_users()
    return render_template('manage_users.html', users=users)

@app.route('/luggage')
def luggage():
    return render_template('luggage.html', flights=airport_controller.flights)

@app.post('/add_luggage')
def add_luggage():
    flight_id = request.form['flight_id']
    passenger_id = request.form['passenger_id']
    luggage_id = request.form['luggage_id']
    weight = request.form['weight']
    status = request.form['status']

    try:
        airport_controller.log_new_luggage(flight_id, passenger_id, luggage_id, weight, status)
        flash(f"Luggage {luggage_id} added successfully.", 'success')
    except Exception as e:
        flash(f"Failed to add luggage: {str(e)}", 'danger')

    return redirect(url_for('luggage'))

@app.post('/update_luggage_status')
def update_luggage_status():
    luggage_id = request.form['luggage_id']
    status = request.form['status']

    try:
        airport_controller.update_luggage_status(luggage_id, status)
        flash(f"Luggage {luggage_id} status updated to {status}.", 'success')
    except Exception as e:
        flash(f"Failed to update luggage status: {str(e)}", 'danger')

    return redirect(url_for('luggage'))


# Check this file was run directly
if __name__ == '__main__':
    
    # Initialize the AirportController
    airport_controller = AirportController()

    # Run the Flask app
    app.run(debug=True)

