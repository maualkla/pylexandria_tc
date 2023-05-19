## Flask API for adminde-tc project.
## Pylexandria Project.
## Coded by: Mauricio Alcala (@maualkla)
## Date: May 2023.
## More info at @intmau in twitter or in http://maualkla.com
## Description: API for the services required by the adminde-tc proyect.

## Imports
from flask import Flask, jsonify, request, render_template
from firebase_admin import credentials, firestore, initialize_app
from config import Config
import os, rsa, bcrypt

## Initiate Public and private key
publicKey, privateKey = rsa.newkeys(512)

## Initialize Flask App
app = Flask(__name__)

## Setup env vars
app.config.from_object(Config)

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
        lemail = request.json['email']
        lpass = request.json['pcode']
        user = users_ref.document(lemail).get()
        user = user.to_dict()
        if user != None: 
            encr_req = encrypt(lpass)
            requ = encr_req.decode('utf-8')
            fire = user['pcode'].decode('utf-8')
            if requ == fire:
                exists = False
                tokensitos = tokens_ref.where('user', '==', lemail)
                for tok in tokensitos.stream():
                    exists = True
                    deleteToken(tok.id)
                token = tokenGenerator(lemail, False)
                return jsonify(token), 200
            else: 
                return jsonify({"status": "User or password is incorrect"}), 401
        else:
            return jsonify({"status": "User not yet registered"}), 404
    except Exception as e: 
        return {"status": "An error Occurred", "error": e}
    
## Login deployment service
@app.route("/login", methods=['GET'])
def login():
    print("/login")
    print(request.args.get('user'))
    print(request.args.get('pass'))
    return 500

## Sign up service
@app.route('/vsignup', methods=['POST'])
def vsignup():
    try:
        email = request.json['email']
        user = users_ref.document(email).get()
        if user != None:
            _pcode = request.json['pcode']
            pwrd = encrypt(_pcode)
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
            response = users_ref.document(email).set(objpay)
            return jsonify({"Status":"Success"}), 202 ##jsonify(objpay), 202
        else:
            return jsonify({"error": True, "errorMessage": "Email already registered" }), 409
    except Exception as e:
        return {"status": "An error Occurred", "error": e}

## Auth a token.
@app.route('/vauth', methods=['POST'])
def vtoken():
    try:
        vauth = tokenValidator(request.json['user'], request.json['id'])
        return vauth
    except Exception as e:
        return e

## API Status
@app.route('/status')
def status():
    return "<p>App Status: <markup style='color:green'>Running fine</markup></p>"


########################################
### Helpers ############################
########################################

## return String (lenght)
def randomString(_length):
    try:
        print(" >> randomString() helper.")
        import random, string
        output_str = ''.join(random.choice(string.ascii_letters) for i in range(_length))
        return output_str
    except Exception as e:
        return {"status": "An error Occurred", "error": e}

## return userId
def idGenerator():
    try:
        print(" >> idGenerator() helper.")
        from datetime import datetime
        now = datetime.now()
        userId = now.strftime("%d%m%YH%M%S")
        userId = randomString(2) + userId + randomString(10)
        return userId
    except Exception as e:
        return {"status": "An error Occurred", "error": e}

## token generator
def tokenGenerator(_user, _ilimited):
    try:
        print(" >> tokenGenerator() helper.")
        from datetime import datetime, timedelta
        current_date_time = datetime.now()
        token = idGenerator()
        if _ilimited:
            new_date_time = current_date_time + timedelta(days=180)
        else:
            new_date_time = current_date_time + timedelta(hours=72)
        new_date_time = new_date_time.strftime("%d%m%YH%M%S")
        tobj = {
            "id" : token,
            "expire" : new_date_time,
            "user": _user
        }
        if tokens_ref.document(token).set(tobj):
            return tobj
        else: 
            return {"status": "Error", "errorStatus": "An error ocurred while creating the token, try again."}
    except Exception as e:
        return {"status": "An error Occurred", "error": e}

## Token validation
def tokenValidator(_user, _token):
    try:
        print(" >> tokenValidator() helper.")
        from datetime import datetime
        current_date_time = datetime.now()
        current_date_time = current_date_time.strftime("%d%m%YH%M%S")
        new_current_date_time = datetime.strptime(current_date_time, '%d%m%YH%M%S')
        vauth = tokens_ref.document(_token).get()
        if vauth != None:
            try:
                objauth = vauth.to_dict()
                expire_date = objauth['expire']
                new_expire_date = datetime.strptime(expire_date, '%d%m%YH%M%S')
                if new_current_date_time.date() < new_expire_date.date():
                    return jsonify({"status": "valid"})
                else: 
                    deleteToken(vtoken)
                    return jsonify({"status": "expired"})
            except Exception as e:
                return {"status": "error"}      
        else:
            return jsonify({"status": "invalid token"})
    except Exception as e:
        return {"status": "An error Occurred", "error": e}

## Delete Token
def deleteToken(_id):
    try:
        print(" >> deleteToken() helper.")
        if tokens_ref.document(_id).delete():
            return True
        else: 
            return False
    except Exception as e:
        return {"status": "An error Occurred", "error": e}

## Encrypt
def encrypt(_string):
    try:    
        print(" >> encrypt() helper.")
        bc_salt = app.config['CONF_SALT_KEY']
        salt = bc_salt.encode('utf-8')
        bytes_pwd = _string.encode('utf-8')
        hashed_pwd = bcrypt.hashpw(bytes_pwd, salt)
        return hashed_pwd
    except Exception as e:
        return {"status": "An error Occurred", "error": e}

## Decrypt
def decrypt(_string):
    
    return False

if __name__ == '__main__':
    app.run(debug=True, port=5000)