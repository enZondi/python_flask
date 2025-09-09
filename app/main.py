from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Oracle APEX login URL
APEX_LOGIN_URL = "https://oracleapex.com/ords/mrelokusa/employee/login"

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    response = requests.put(APEX_LOGIN_URL, json=data)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
