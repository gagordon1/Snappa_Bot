#READ groupme import json
from flask import Flask, request, redirect, g, render_template, jsonify


PORT = 8080

app = Flask(__name__)


@ app.route("/", methods=["GET", "POST"])
def home():
    print(request.data)
    print(request.text)
    if request.method == "GET":
        return "WELCOME TO SNAPPA BOT BITCH"
    elif request.method == "POST":
        return request.data
    else:
        return "WELCOME TO SNAPPA BOT"

if __name__ == "__main__":
    app.run(debug=True, port=PORT)