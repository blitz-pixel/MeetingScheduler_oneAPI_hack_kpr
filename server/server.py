from flask import Flask, request, jsonify, redirect, session, url_for
import requests
from pymongo import MongoClient
from urllib.parse import quote_plus
from flask_cors import CORS
from flask_session import Session
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
password = quote_plus('charan@db')

app.config['SECRET_KEY'] = os.getenv('SESSION_SECRET_KEY') # Set your secret key for session
app.config['SESSION_TYPE'] = 'filesystem'  # Use filesystem session
Session(app)  # Initialize the session

# MongoDB connection
client = MongoClient(f"mongodb+srv://AI-Meeting-Scheduler:{password}@cluster0.kikcm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['AI-Meeting-Scheduler']
user_collection = db['users']

# Google OAuth credentials
app.config['CLIENT_ID'] = os.getenv('CLIENT_ID')
app.config['CLIENT_SECRET'] = os.getenv('CLIENT_SECRET')

GOOGLE_REDIRECT_URI = 'http://127.0.0.1:5001/auth-google'  

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the AI Meeting Scheduler!'})

# Route for Google login
@app.route('/login-google')
def login_google():
    return redirect(
        f"https://accounts.google.com/o/oauth2/v2/auth?client_id={app.config['CLIENT_ID']}&redirect_uri={GOOGLE_REDIRECT_URI}&response_type=code&scope=https://www.googleapis.com/auth/calendar.readonly"
    )

# Route for handling Google authentication callback
@app.route('/auth-google')
def auth_google():
    code = request.args.get('code')
    token_url = 'https://oauth2.googleapis.com/token'
    data = {
        'code': code,
        'client_id': app.config['CLIENT_ID'],
        'client_secret': app.config['CLIENT_SECRET'],
        'redirect_uri': GOOGLE_REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    
    # Get access token
    response = requests.post(token_url, data=data)
    token_info = response.json()
    
    session['user'] = {
        'access_token': token_info['access_token'],
        'refresh_token': token_info.get('refresh_token')
    }
    
    return redirect(url_for('get_calendar_events'))

# Route to fetch calendar events
@app.route('/calendar-events', methods=['GET'])
def get_calendar_events():
    if 'user' not in session:
        return redirect(url_for('login_google'))

    user_info = session['user']
    access_token = user_info['access_token']

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    events_url = 'https://www.googleapis.com/calendar/v3/calendars/primary/events'

    # Fetch calendar events
    response = requests.get(events_url, headers=headers)
    events = response.json().get('items', [])

    # Extract and format events
    busy_free_times = []
    for event in events:
        event_summary = event.get('summary', 'free')  
        if not event_summary:
            event_summary = 'free'
        busy_free_times.append({
            'summary': event.get('summary'),
            'start': event.get('start', {}).get('dateTime'),
            'end': event.get('end', {}).get('dateTime'),
        })

    return jsonify(busy_free_times)


# Register user route
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
    if not username or not password or not email:
        return jsonify({'message': 'Please provide username, email, and password.'}), 400
    
    existing_user = user_collection.find_one({'email': email})
    if existing_user:
        return jsonify({'message': 'User already exists.'}), 400
    
    user_collection.insert_one({
        'username': username,
        'password': password,  
        'email': email  
    })
    
    return jsonify({'message': 'User successfully registered!'}), 201

# Login user route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = user_collection.find_one({'email': email})
    if not user or user['password'] != password:
        return jsonify({'message': 'Invalid credentials!'}), 401

    return jsonify({'message': 'Login successful!'})


if __name__ == '__main__':
    app.run(debug=True, port=5001)
