# python_files/apex_api.py

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from apex import (
    login_employee,
    login_employee_qr,
    get_bookings,
    checkout_booking,
    checkin_booking,
    save_qr_image
)

app = Flask(__name__)
CORS(app)  # allow requests from any origin

# -----------------------------
# In-memory session storage (for simplicity)
# -----------------------------
sessions = {}

# -----------------------------
# ROUTES
# -----------------------------
@app.route("/login", methods=["POST"])
def password_login():
    data = request.json
    try:
        token = login_employee(data["employee_code"], data["password"])
        sessions[data["employee_code"]] = token
        return jsonify({"token": token, "employee_code": data["employee_code"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/login/qr", methods=["POST"])
def qr_login():
    data = request.json
    try:
        token = login_employee_qr(data["qr_code"])
        sessions[data["qr_code"]] = token
        return jsonify({"token": token, "qr_code": data["qr_code"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/bookings", methods=["GET"])
def bookings():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Missing Authorization header"}), 401
    try:
        bookings_list = get_bookings()
        return jsonify(bookings_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/checkout", methods=["POST"])
def checkout():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Missing Authorization header"}), 401
    data = request.json
    try:
        booking = checkout_booking(
            employee_id=data["employee_id"],
            equipment_id=data["equipment_id"],
            quantity=data["quantity_booked"],
            due_date=data["due_date"],
            admin_id=data["admin_id"],
            notes=data["notes"]
        )
        return jsonify(booking)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/checkin", methods=["PUT"])
def checkin():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Missing Authorization header"}), 401
    data = request.json
    try:
        booking_id = data["booking_id"]
        result = checkin_booking(booking_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/generate_qr", methods=["POST"])
def generate_qr():
    data = request.json
    value = data.get("value")
    filename = data.get("filename")
    try:
        path = save_qr_image(value, filename)
        return jsonify({"path": path})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render-assigned port
    app.run(host="0.0.0.0", port=port, debug=True)
