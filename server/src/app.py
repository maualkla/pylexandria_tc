## Flask API for adminde-tc project.
## Pylexandria Project.
## Coded by: Mauricio Alcala (@maualkla)
## Date: May 2023.
## More info at @intmau in twitter or in http://maualkla.com
## Description: API for the services required by the adminde-tc proyect.

## Imports
from flask import Flask, jsonify, request, render_template
from firebase_admin import credentials, firestore, initialize_app
import os, rsa

## Initiate Public and private key
publicKey, privateKey = rsa.newkeys(512)

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
        if user != None: 
            encr_req = encrypt(password)
            print(" Encrupted request password: ")
            print(encr_req)
            print(" firestore DB pwrd: ")
            print(user['pcode'])
            if user['pcode'] == encr_req:
                print("user: " + email + " pword: " + user['pcode'] + " request.pword: " + request.json['pcode'])
                print(" GET TOKENS ")
                exists = False
                tokensitos = tokens_ref.where('user', '==', email)
                for tok in tokensitos.stream():
                    print(f"{tok.id} => {tok.to_dict()}")
                    exists = True
                    deleteToken(tok.id)
                ##print(tokensitos.to_dict())
                print(" THOSE WHERE THE TOKENS")
                print("Go to token generator")
                token = tokenGenerator(email, False)
                print("token returned")
                print(token)
                return jsonify(token), 200
                ##return jsonify({"status": "success"}), 200
            else: 
                return jsonify({"status": "User or password is incorrect"}), 401
        else:
            return jsonify({"status": "User not yet registered"}), 404
    except Exception as e: 
        return jsonify({"status": "Error"}), 500

## Sign up service
@app.route('/vsignup', methods=['POST'])
def vsignup():
    try:
        print(">>> Sign Up Service: ")
        print(request.json['email'])
        email = request.json['email']
        user = users_ref.document(email).get()
        ##user = user.to_dict()
        if user != None:
            print(request.json['pcode'])
            _pcode = request.json['pcode']
            print(" User exist: ")
            pwrd = encrypt(_pcode)
            print(" request password encrypted: ")
            print(pwrd)
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
            print(objpay)
            response = users_ref.document(email).set(objpay)
            print(response)
            print( ">>> Sending response 202")
            return jsonify({"Status":"Success"}), 202 ##jsonify(objpay), 202
        else:
            return jsonify({"error": True, "errorMessage": "Email already registered" }), 409
    except Exception as e:
        return {"status": "An error Occurred", "error": e}

## Generate a token.
@app.route('/vauth', methods=['POST'])
def vtoken():
    vauth = tokenValidator(request.json['user'], request.json['id'])
    return vauth


## API Status
@app.route('/status')
def status():
    return "<p>App Status: <markup style='color:green'>Running fine</markup></p>"


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
            new_date_time = current_date_time + timedelta(hours=72)
        print(" creation date: ")
        print(new_date_time)
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
        return {"status": "An error Occurred", "error": e}

## Token validation
def tokenValidator(user, vtoken):
    try:
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
            new_expire_date = datetime.strptime(expire_date, '%d%m%YH%M%S')
            print("current date: " + str(type(new_current_date_time)) + " expired_date: " + str(type(new_expire_date)))
            print("current date: ")
            print(new_current_date_time)
            print(" expire_date: ")
            print(new_expire_date)
            if new_current_date_time.date() < new_expire_date.date():
                return jsonify({"status": "valid"})
            else: 
                ## delete token
                print("go to delete token")
                deleteToken(vtoken)
                return jsonify({"status": "expired"})        
        else:
            return jsonify({"status": "invalid token"})
    except Exception as e:
        return {"status": "An error Occurred", "error": e}

## Delete Token
def deleteToken(idTok):
    try:
        print(" in deleting token: ")
        if tokens_ref.document(idTok).delete():
            print("token deleted")
            return True
        else: 
            print("token not deleted")
            return False
    except Exception as e:
        return {"status": "An error Occurred", "error": e}

## Encrypt
def encrypt(_string):
    
    message = _string
    encMessage = rsa.encrypt(message.encode(), publicKey)
    print("original string: ", message)
    print("encrypted string: ", encMessage)
    decMessage = rsa.decrypt(encMessage, privateKey).decode()
    print("decrypted string: ", decMessage)
    return encMessage

## Decrypt
def decrypt(_string):
    message = _string
    decMessage = rsa.decrypt(message, privateKey).decode()
    print("decrypted string: ", decMessage)
    return decMessage

if __name__ == '__main__':
    app.run(debug=True, port=5000)