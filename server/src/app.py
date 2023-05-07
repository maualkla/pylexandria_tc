## Flask API for adminde-tc project.
## Pylexandria Project.
## Coded by: Mauricio Alcala (@maualkla)
## Date: May 2023.
## More info at @intmau in twitter or in http://maualkla.com
## Description: API for the services required by the adminde-tc proyect.

## Imports
from flask import Flask, jsonify, request, render_template
from firebase_admin import credentials, firestore, initialize_app
import os 

## Initialize Flask App
app = Flask(__name__)

## Initialize Firestone DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
users_ref = db.collection('users')

## @TO_BE_DELETED 
# sample helloworld
@app.route('/helloworld')
def hello_world():
    import requests

    url = 'http://localhost:5000/vlogin'
    data = {
        "user": "maualkla",
        "email": "mauricio@adminde.com",
        "password": "helloadminde2023"
        }
    headers = {'Content-type': 'application/json'}

    response = requests.post(url, json=data, headers=headers)
    print(response)
    ##print(response.json())
    return 'Hello World!'

## @TO_BE_DELETED
# Landing page
@app.route('/')
def landing():
    return render_template('index.html')

## @TO_BE_DELETED
# Sample service
@app.route('/service', methods=['GET'])
def service():
    data = request.get_json()
    if data:
        return jsonify({
            "status": "connected",
            "code": 200
        })
    else:
        return jsonify({
            "status": "Error",
            "code": 500
        })

## Login service    
@app.route('/vlogin', methods=['POST'])
def vlogin():
    try:
        email = request.json['email']
        password = request.json['password']
        user = users_ref.document(email).get()
        user = user.to_dict()
        if user['pcode'] == password:
            return jsonify({"status": "Successfully Logged"}), 200
        else: 
            return jsonify({"status": "User or password not match"}), 401
    except Exception as e: 
        return jsonify({"status": "Error"}), 500

## Sign up service
@app.route('/vsignup', methods=['POST'])
def vsignup():
    try:
        email = request.json['email']
        users_ref.document(email).set(request.json)
        return jsonify({"success": True}), 202
    except Exception as e:
        return {"status": "An error Occurred", 
                "error": e}



if __name__ == '__main__':
    app.run(debug=True, port=int(os.envirom.get('PORT', 8080)))
