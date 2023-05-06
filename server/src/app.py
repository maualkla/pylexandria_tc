## Sample code

from flask import Flask, jsonify, request, render_template
## Import firebase object
from firebase import firebase
from firebase_admin import credentials, firestore, initialize_app
import os

app = Flask(__name__)


## Get data from our firebase realtime db
firebase = firebase.FirebaseApplication('https://adminde-tc-default-rtdb.firebaseio.com/', None)

@app.route('/helloworld')
def hello_world():
    ##print(firebase.get('/users', None))
    result = firebase.get('/users', None)
    return str(result)

@app.route('/')
def landing():
    return render_template('index.html')
    
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

if __name__ == '__main__':
    app.run(debug=True, port=int(os.envirom.get('PORT', 8080)))
