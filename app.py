## Sample code

from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

@app.route('/helloworld')
def hello_world():
    return 'Hello, World!'

@app.route('/')
def landing():
    return render_template('/templates/index.html')
    
@app.route('/service', methods=['GET'])
def service():
    data = request.get_json()
    if data is None:
        return jsonify({})
    else:
        return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
