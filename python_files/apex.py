from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Your Oracle APEX login URL
APEX_LOGIN_URL = "https://oracleapex.com/ords/mrelokusa/employee/login"

@app.route("/login", methods=["POST"])
def login():
    data = request.json  # Expect {"EMPLOYEE_CODE": "...", "PASSWORD": "..."}
    
    # Forward login request to APEX
    response = requests.put(APEX_LOGIN_URL, json=data)
    
    # Return APEX JSON response directly
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=True)
