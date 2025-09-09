from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

BASE_URL = "https://oracleapex.com/ords/mrelokusa"

# -----------------------------
# Login
# -----------------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    r = requests.post(f"{BASE_URL}/employee/login", json=data)
    r.raise_for_status()
    return jsonify(r.json())

@app.route("/login/qr", methods=["POST"])
def login_qr():
    data = request.get_json()
    r = requests.post(f"{BASE_URL}/employee/login/qr", json=data)
    r.raise_for_status()
    return jsonify(r.json())

# -----------------------------
# Bookings
# -----------------------------
@app.route("/bookings", methods=["GET"])
def get_bookings():
    # Optional: filter by employee_id header
    employee_id = request.headers.get("X-Employee-ID")
    url = f"{BASE_URL}/employee/bookings/active"
    r = requests.get(url)
    r.raise_for_status()
    bookings = r.json()
    if employee_id:
        bookings = [b for b in bookings if str(b["employee_id"]) == str(employee_id)]
    return jsonify(bookings)

@app.route("/checkout", methods=["POST"])
def checkout():
    data = request.get_json()
    r = requests.post(f"{BASE_URL}/admin/checkout", json=data)
    r.raise_for_status()
    return jsonify(r.json())

@app.route("/checkin", methods=["PUT"])
def checkin():
    data = request.get_json()
    r = requests.put(f"{BASE_URL}/employee/checkin", json=data)
    r.raise_for_status()
    return jsonify(r.json())
