## Sample code

from flask import Flask, jsonify, request, render_template


## Import firebase object
from firebase_admin import credentials, firestore, initialize_app
from firebase import firebase

import os   ##, pyrebase

app = Flask(__name__)


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

####

## Get data from our firebase realtime db
##firebase = firebase.FirebaseApplication('https://adminde-tc-default-rtdb.firebaseio.com/', None)

## sample helloworld
@app.route('/helloworld')
def hello_world():
    ##print(firebase.get('/users', None))
    ##result = firebase.get('/users', None)
    ##return str(result)
    return 'Hello World!'

## Landing page
@app.route('/')
def landing():
    return render_template('index.html')

## Sample service
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
    """ ## Old code
    data = request.get_json()
    print(data)
    result = firebase.get('/users', None)
    result[0]
    if data['user'] == 'maualkla' and data['password'] == 'hola':
        return {"status": "loged successfull"}
    else:
        return {"status": "user not found"}
    """
    ##fbinit = initialize_app(config)
    ##print(fbinit)
    return {"status": "true"}



@app.route('/vsignup', methods=['POST'])
def vsignup():
    """
    data = request.get_json()
    print(data)
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    user = auth.create_user_with_email_and_password(data['email'], data['password'])
    print(user)
    """

    return {"status": "true"}



if __name__ == '__main__':
    app.run(debug=True, port=int(os.envirom.get('PORT', 8080)))
