# app.py
from flask import Flask, jsonify, request

app = Flask(__name__)

# Home route
@app.route("/")
def home():
    return "🎉 Welcome to Flask API!"

# GET endpoint
@app.route("/hello", methods=["GET"])
def hello():
    return jsonify({"message": "Hello from Flask!"})

# POST endpoint
@app.route("/add", methods=["POST"])
def add_numbers():
    data = request.json
    result = data["a"] + data["b"]
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
