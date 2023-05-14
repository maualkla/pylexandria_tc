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
        password = request.json['pcode']
        user = users_ref.document(email).get()
        user = user.to_dict()
        print("user: " + email + " pword: " + password + " request.pword: " + request.json['pcode'])
        if user['pcode'] == password:
            print("Go to token generator")
            token = tokenGenerator(email, False)
            print("token returned")
            print(token)
            return jsonify(token), 200
            ##return jsonify({"status": "success"}), 200
        else: 
            return jsonify({"status": "User or password is incorrect"}), 401
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
            pwrd = request.json['pcode'] ##hash(request.json['pcode'])
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
            return jsonify(objpay), 202
        else:
            return jsonify({"error": True, "errorMessage": "Email already registered" }), 409
    except Exception as e:
        return {"status": "An error Occurred", 
                "error": e}

## Generate a token.
@app.route('/vauth', methods=['POST'])
def vtoken():
    vauth = tokenValidator(request.json['user'], request.json['id'])
    return vauth


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
    userId = randomString(2) + userId + randomString(10)
    return userId

## token generator
def tokenGenerator(user, ilimited):
    try:
        from datetime import datetime, timedelta
        current_date_time = datetime.now()
        token = idGenerator()
        if ilimited:
            new_date_time = current_date_time + timedelta(days=180)
        else:
            new_date_time = current_date_time ##+ timedelta(hours=72)
        new_date_time = new_date_time.strftime("%d%m%YH%M%S")
        print("date: "+new_date_time)
        tobj = {
            "id" : token,
            "expire" : new_date_time,
            "user": user
        }
        print("inside tokenGenerator")
        print(tobj)
        print(tokens_ref.document(token).set(tobj))
        return tobj
    except Exception as e:
        return {"status": "An error Occurred", 
                "error": e}

## Token validation
def tokenValidator(user, vtoken):
    from datetime import datetime
    current_date_time = datetime.now()
    current_date_time = current_date_time.strftime("%d%m%YH%M%S")
    new_current_date_time = datetime.strptime(current_date_time, '%d%m%YH%M%S')

    print("Entramos en token validator")
    print("token: "+vtoken+" user: "+user)
    vauth = tokens_ref.document(vtoken).get()
    ###vauth.to_dict()
    
    print(vauth)
    if vauth != None:
        objauth = vauth.to_dict()
        expire_date = objauth['expire']
        print("date to expire.")
        print(objauth['expire'])
        new_expire_date = datetime.strptime(expire_date, '%d%m%YH%M%S')
        print("current date: " + str(type(new_current_date_time)) + " expired_date: " + str(type(new_expire_date)))
        if new_current_date_time.date() > new_expire_date.date():
            return jsonify({"status": "valid token"})
        else: 
            return jsonify({"status": "Token expired"})        
    else:
        return jsonify({"status": "invalid token"})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
