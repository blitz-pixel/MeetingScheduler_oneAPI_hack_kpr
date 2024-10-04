from flask import Flask, request, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from urllib.parse import quote_plus
from functools import wraps

app = Flask(__name__)


password = quote_plus('charan@db')

# Use the encoded password in the connection string
client = MongoClient(f"mongodb+srv://AI-Meeting-Scheduler:{password}@cluster0.kikcm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['AI-Meeting-Scheduler']
user_collection = db['users']

# Secret key for JWT
app.config['SECRET_KEY'] = 'your_secret_key'

# Token Required Decorator (optional for protected routes)
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = user_collection.find_one({'_id': data['user_id']})
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)
    
    return decorated

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the AI Meeting Scheduler!'})
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
    
    hashed_password = generate_password_hash(password)
    
    user_collection.insert_one({
        'username': username,
        'password': hashed_password,
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
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid credentials!'}), 401

    # Generate JWT token
    token = jwt.encode({
        'user_id': str(user['_id']),
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
    }, app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({'token': token})

if __name__ == '__main__':
    app.run(debug=True,port=5001)
