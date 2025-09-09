from flask import Flask, request, jsonify
from python_files import apex  # relative import

app = Flask(__name__)

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    employee_code = data.get("employee_code")
    password = data.get("password")
    if not employee_code or not password:
        return jsonify({"error": "employee_code and password required"}), 400

    try:
        token = apex.login_employee(employee_code, password)
        return jsonify({"token": token})
    except requests.exceptions.HTTPError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Login failed"}), 500

@app.route("/login_qr", methods=["POST"])
def login_qr():
    data = request.get_json()
    qr_code = data.get("qr_code")
    if not qr_code:
        return jsonify({"error": "qr_code required"}), 400

    try:
        token = apex.login_employee_qr(qr_code)
        return jsonify({"token": token})
    except requests.exceptions.HTTPError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "QR Login failed"}), 500

@app.route("/bookings", methods=["GET"])
def bookings():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Authorization header required"}), 401
    token = token.replace("Bearer ", "")
    try:
        data = apex.get_bookings(token)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/bookings/<int:booking_id>/checkout", methods=["POST"])
def checkout(booking_id):
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Authorization header required"}), 401
    token = token.replace("Bearer ", "")
    try:
        data = apex.checkout_booking(token, booking_id)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
