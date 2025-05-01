import bcrypt
import json
import os
from datetime import datetime, timedelta

USER_FILE = "users.json"
LOG_FILE = "logs.txt"

# This loads all users from file
def load_users():
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w", encoding='utf-8') as f:
            json.dump({}, f)
        return {}
    with open(USER_FILE, "r", encoding='utf-8') as f:
        return json.load(f)


# Saves all users to the file
def save_users(users):
    try:
        with open(USER_FILE, "w", encoding='utf-8') as f:
            json.dump(users, f, indent=4)
    except Exception as e:
        print(f"Error saving users: {e}")


# It logs when you logged in (time/date)
def log_event(event):
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {event}\n")

# Register new user with secure hash system
def register(username, password, role="user"):
    users = load_users()

    if username in users:
        return False, "Username already exists."

    # Hash the password using bcrypt and ensure the hash is stored as a string
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  # .decode() to make sure it's stored as string

    users[username] = {
        "password": hashed,
        "role": role,
        "carbon_footprint": 0.0,
        "email": "",
        "phone": "",
        "failed_attempts": 0,
        "lockout_until": None
    }

    save_users(users)
    return True, f"User '{username}' registered as '{role}'."


# Account login code
def login(username, password):
    users = load_users()
    
    # Check if user exists
    if username not in users:
        return False, "User not found.", None

    user_data = users[username]

    # Account lockout mechanism
    lockout_until = user_data.get("lockout_until")
    if lockout_until:
        try:
            lockout_time = datetime.fromisoformat(lockout_until)
            if datetime.now() < lockout_time:
                return False, f"Account locked until {lockout_until}", None
        except ValueError:
            user_data["lockout_until"] = None

    # Get the hashed password from the database (it will be stored as a string)
    stored_hash = user_data["password"]

    print("Entered password: ", password)
    print("Stored hashed password: ", stored_hash)
    print(f"Password comparison: {bcrypt.checkpw(password.encode(), stored_hash.encode())}")

    
    # Compare entered password with stored hash
    if bcrypt.checkpw(password.encode(), stored_hash.encode()):  # Ensure both are byte-encoded before comparison
        user_data["failed_attempts"] = 0
        user_data["lockout_until"] = None
        save_users(users)
        return True, "Login successful.", user_data["role"]
    else:
        user_data["failed_attempts"] = user_data.get("failed_attempts", 0) + 1

        if user_data["failed_attempts"] >= 3:
            lockout_time = datetime.now() + timedelta(minutes=5)
            user_data["lockout_until"] = lockout_time.isoformat()
            message = f"Account locked due to multiple failed attempts. Try again after {lockout_time.strftime('%Y-%m-%d %H:%M:%S')}"
        else:
            message = f"Incorrect password. {3 - user_data['failed_attempts']} attempt(s) left."

        save_users(users)
        return False, message, None

