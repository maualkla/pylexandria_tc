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

### Objects

config = {
        "apiKey": "AIzaSyDv5ePfMX3CgKRsRllNhTDw04YaS_uEaok",
        "authDomain": "adminde-tc.firebaseapp.com",
        "databaseURL": "https://adminde-tc-default-rtdb.firebaseio.com",
        "projectId": "adminde-tc",
        "storageBucket": "adminde-tc.appspot.com",
        "messagingSenderId": "78456937956",
        "appId": "1:78456937956:web:6a9cb05e437dcfcb117bf1",
        "measurementId": "G-VCBNFR07G2"
    }

## @TO_BE_DELETED 
# sample helloworld
@app.route('/helloworld')
def hello_world():
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
   
    return {"status": "true"}

## Sign up service
@app.route('/vsignup', methods=['POST'])
def vsignup():
    try:
        email = request.json['email']
        users_ref.document(email).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return {"status": "An error Occurred", 
                "error": e}



if __name__ == '__main__':
    app.run(debug=True, port=int(os.envirom.get('PORT', 8080)))
