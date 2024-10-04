import datetime
from flask import Flask, request, jsonify, redirect, session, url_for
import requests
from pymongo import MongoClient
from urllib.parse import quote_plus
from flask_cors import CORS
from flask_session import Session
from dotenv import load_dotenv
import os,re
load_dotenv()
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


app.config['SECRET_KEY'] = os.getenv('SESSION_SECRET_KEY') # Set your secret key for session
app.config['SESSION_TYPE'] = 'filesystem'  # Use filesystem session
Session(app)  # Initialize the session

# MongoDB connection
client = MongoClient(os.getenv('MONGO_URI'))
db = client['AI-Meeting-Scheduler']
user_collection = db['users']
time_collection = db['Time']

app.config['CLIENT_ID'] = os.getenv('CLIENT_ID')
app.config['CLIENT_SECRET'] = os.getenv('CLIENT_SECRET')

GOOGLE_REDIRECT_URI = 'http://127.0.0.1:5001/auth-google'  

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the AI Meeting Scheduler!'})

# Route for Google login
@app.route('/login-google')
def login_google():
    scopes = "https://www.googleapis.com/auth/calendar.readonly https://www.googleapis.com/auth/userinfo.email"
    return redirect(
        f"https://accounts.google.com/o/oauth2/v2/auth?client_id={app.config['CLIENT_ID']}&redirect_uri={GOOGLE_REDIRECT_URI}&response_type=code&scope={scopes}"
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
    
    # Fetch user info using access token
    user_info_response = requests.get(
        'https://www.googleapis.com/oauth2/v2/userinfo',
        headers={'Authorization': f"Bearer {token_info['access_token']}"}
    )
    
    user_info = user_info_response.json()

     
    session['user'] = {
        'access_token': token_info['access_token'],
        'refresh_token': token_info.get('refresh_token'),
        'email': user_info.get('email')
    }

    # Add email to the session
    # session['user']['email'] = user_info.get('email')

    return redirect(url_for('get_calendar_events'))

@app.route('/calendar-events', methods=['GET'])
def get_calendar_events():
    if 'user' not in session:
        return redirect(url_for('login_google'))

    user_info = session['user']
    access_token = user_info['access_token']
    email  = user_info['email']
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    events_url = 'https://www.googleapis.com/calendar/v3/calendars/primary/events'

    # Fetch calendar events
    response = requests.get(events_url, headers=headers)
    
    # Check for errors in the response
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch calendar events'}), response.status_code

    events = response.json().get('items', [])
    separators = r'[+t]' 
    # Extract and format events
    busy_free_times = []
    for event in events:
        event_summary = event.get('summary', 'free')  
        start_time = event.get('start', {}).get('dateTime')
        Start_time = start_time.split('T')[1].split('+')[0] if start_time else None
        
        end_time = event.get('end', {}).get('dateTime')
        End_time = end_time.split('T')[1].split('+')[0] if end_time else None
        
        # Extract start and end dates
        start_date = start_time.split("T")[0] if start_time else None
        end_date = end_time.split("T")[0] if end_time else None
        utc_offset = start_time[-6:] if start_time and (start_time[-6] == '+' or start_time[-6] == '-') else None
        
        busy_free_times.append({    
            'email' : email,
            'summary': event_summary,  # Event title
            'start_time': Start_time,  # Start time of the event
            'end_time': End_time,      # End time of the event
            'start_date': start_date,  # Start date of the event
            'end_date': end_date,       # End date of the event
            'UTC': utc_offset
        })

        time_collection.insert_one({
            'email' : email,
            'summary': event_summary,  # Event title
            'start_time': Start_time,  # Start time of the event
            'end_time': End_time,      # End time of the event
            'start_date': start_date,  # Start date of the event
            'end_date': end_date,       # End date of the event
            'UTC': utc_offset
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
