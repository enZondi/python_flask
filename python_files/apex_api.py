# python_files/apex_api.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import python_files.apex as apex_client  # your existing Python client
import requests

app = Flask(__name__)
CORS(app)  # allow cross-origin requests

# -----------------------------
# Config
# -----------------------------
REQUEST_TIMEOUT = 10  # seconds

# -----------------------------
# Employee Login
# -----------------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if not data or "employee_code" not in data or "password" not in data:
        return jsonify({"error": "Missing employee_code or password"}), 400
    try:
        token = apex_client.login_employee(data["employee_code"], data["password"])
        return jsonify({"token": token})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 502
    except KeyError:
        return jsonify({"error": "Invalid response from APEX"}), 502

@app.route("/login/qr", methods=["POST"])
def login_qr():
    data = request.json
    if not data or "qr_code" not in data:
        return jsonify({"error": "Missing qr_code"}), 400
    try:
        token = apex_client.login_employee_qr(data["qr_code"])
        return jsonify({"token": token})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 502
    except KeyError:
        return jsonify({"error": "Invalid response from APEX"}), 502

# -----------------------------
# Bookings
# -----------------------------
@app.route("/bookings/active", methods=["GET"])
def get_bookings():
    try:
        bookings = apex_client.get_bookings()
        return jsonify(bookings)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 502

@app.route("/checkout", methods=["POST"])
def checkout():
    data = request.json
    required_fields = ["employee_id", "equipment_id", "quantity_booked", "due_date", "admin_id", "notes"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": f"Missing fields, required: {required_fields}"}), 400
    try:
        result = apex_client.checkout_booking(
            data["employee_id"],
            data["equipment_id"],
            data["quantity_booked"],
            data["due_date"],
            data["admin_id"],
            data["notes"]
        )
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 502

@app.route("/checkin", methods=["PUT"])
def checkin():
    data = request.json
    if not data or "booking_id" not in data:
        return jsonify({"error": "Missing booking_id"}), 400
    try:
        result = apex_client.checkin_booking(data["booking_id"])
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 502

# -----------------------------
# QR Code Generation
# -----------------------------
@app.route("/generate_qr", methods=["POST"])
def generate_qr():
    data = request.json
    if not data or "value" not in data or "filename" not in data:
        return jsonify({"error": "Missing value or filename"}), 400
    try:
        path = apex_client.save_qr_image(data["value"], data["filename"])
        return jsonify({"path": path})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------------
# Health Check
# -----------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
