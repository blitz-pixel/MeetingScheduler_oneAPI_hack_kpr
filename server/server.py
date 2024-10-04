from flask import Flask, request, jsonify
from pymongo import MongoClient
from urllib.parse import quote_plus

app = Flask(__name__)

password = quote_plus('charan@db')


client = MongoClient(f"mongodb+srv://AI-Meeting-Scheduler:{password}@cluster0.kikcm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['AI-Meeting-Scheduler']
user_collection = db['users']

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
