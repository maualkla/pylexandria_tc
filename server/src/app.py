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
tokens_ref = db.collection('tokens')

## Login service    
@app.route('/vlogin', methods=['POST'])
def vlogin():
    try:
        email = request.json['email']
        password = request.json['word']
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
        user = users_ref.document(email).get()
        user = user.to_dict()
        if user == None:
            pwrd = hash(request.json['pcode'])
            objpay = {
                "activate": True,
                "alias": request.json['alias'],
                "birthdate": request.json['birthdate'],
                "email": request.json['email'],
                "fname": request.json['fname'],
                "pcode": pwrd,
                "phone": request.json['phone'],
                "pin": request.json['pin'],
                "plan": request.json['plan'],
                "postalCode": request.json['postalCode'],
                "terms": request.json['terms'],
                "type": request.json['type']
            }
            print(users_ref.document(email).set(objpay))
            return jsonify({"success": True}), 202
        else:
            return jsonify({"error": True, "errorMessage": "Email already registered" }), 409
    except Exception as e:
        return {"status": "An error Occurred", 
                "error": e}

## Generate a token.
@app.route('/vauth', methods=['POST'])
def vtoken():
    return True


## API Status
@app.route('/status')
def status():
    return "<p>App Status: <msrkup style='color:green'>Running fine</markup></p>"


########################################
### Helpers ############################
########################################

## return String (lenght)
def randomString(length):
    import random, string
    output_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    return output_str

## return userId
def idGenerator():
    from datetime import datetime
    now = datetime.now()
    userId = now.strftime("%d%m%YH%M%S")
    userId = userId + randomString(5)
    return userId

## token generator
def tokenGenerator(user, ilimited):
    token = idGenerator()
    if ilimited == False:
        ilimited = False
    return True

if __name__ == '__main__':
    app.run(debug=True, port=5000)
