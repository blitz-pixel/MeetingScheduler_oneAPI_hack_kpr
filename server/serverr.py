from flask import Flask, request,jsonify
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb+srv://AI-Meeting-Scheduler:charan@db@cluster0.kikcm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['AI-Meeting-Scheduler']
users_collection = db['users']

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
    if not username or not password or not email:
        return jsonify({'message':'please provide username,email and password.'}),400
    
    existing_user = users_collection.find_one({'email':email})
    if existing_user:
        return jsonify({'message':'user already exists.'}),400
    
    users_collection.insert_one({
        'username' : username,
        'password' : password,
        'email' : email  
    })
    
    return jsonify({'message': 'user sucsessfully registered!'}),201

if __name__ == '__main__':
    app.run(debug=True)
    
