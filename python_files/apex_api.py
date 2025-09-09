from flask import Flask, request, jsonify
import apex
import requests  # Needed for downstream calls

app = Flask(__name__)

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    employee_code = data.get("employee_code")
    password = data.get("password")
    try:
        # MOCK_LOGIN = True ensures we don't call any real APEX server
        token = apex.login_employee(employee_code, password)
        return jsonify({"token": token})
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Downstream request failed: {e}"}), 500

@app.route("/bookings", methods=["GET"])
def bookings():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    try:
        data = apex.get_bookings(token)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/bookings/<int:booking_id>/checkout", methods=["POST"])
def checkout(booking_id):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    try:
        data = apex.checkout_booking(token, booking_id)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
