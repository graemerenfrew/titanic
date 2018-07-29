
from flask import Flask, request
app = Flask(__name__)

@app.route('/api', methods=['POST']) #api will take an input, process it, and return it

def say_hello():
    data = request.get_json(force=True) #we will pass json, so use get_json to get extract the data
    name = data['name']
    return "hello {0}".format(name)

if __name__ == '__main__': # script entry point, the flask app will run on port 10001 - can be any available port
    app.run(port=10001, debug=True,use_reloader=False) # debug = true for troubleshooting in dev