## Flask API for adminde-tc project.
## Pylexandria Project.
## Coded by: Mauricio Alcala (@maualkla)
## Date: May 2023.
## More info at @intmau in twitter or in http://maualkla.com
## Description: API for the services required by the adminde-tc proyect.

from flask import Flask, jsonify, request, render_template


import os 

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


@app.route('/vsignup', methods=['POST'])
def vsignup():

    return {"status": "true"}



if __name__ == '__main__':
    app.run(debug=True, port=int(os.envirom.get('PORT', 8080)))
