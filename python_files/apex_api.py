# python_files/apex_api.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime, timezone
import qrcode
import io

app = Flask(__name__)
CORS(app)

# -----------------------------
# Mock Database / In-Memory Store
# -----------------------------
# Replace with real Oracle APEX calls in production
EMPLOYEES = {
    "EMP001": {"password": "mypassword", "employee_id": 1},
    "EMP002": {"password": "password2", "employee_id": 2},
}

BOOKINGS = [
    {
        "booking_id": 1,
        "equipment_id": 1,
        "employee_id": 1,
        "admin_id": 1,
        "checkout_date": "2025-09-09T03:29:43.107157Z",
        "due_date": "2025-09-16T03:29:43.107157Z",
        "quantity_booked": 1,
        "status": "CHECKED_OUT",
        "notes": "For IoT sensor prototype development",
        "qr_code": "BK-1-20250909032943",
    },
]

# -----------------------------
# Utility Functions
# -----------------------------
def generate_jwt(employee_id: int) -> str:
    # Mock token for simplicity; replace with real JWT
    return f"TOKEN-{employee_id}"

def generate_qr_image(value: str) -> bytes:
    img = qrcode.make(value)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf.read()

# -----------------------------
# Routes
# -----------------------------
@app.route("/login", methods=["POST"])
def login_employee():
    data = request.get_json()
    code = data.get("employee_code")
    pw = data.get("password")
    emp = EMPLOYEES.get(code)
    if emp and emp["password"] == pw:
        token = generate_jwt(emp["employee_id"])
        return jsonify({"token": token}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/login/qr", methods=["POST"])
def login_employee_qr():
    data = request.get_json()
    qr_code = data.get("qr_code")
    booking = next((b for b in BOOKINGS if b["qr_code"] == qr_code), None)
    if booking:
        token = generate_jwt(booking["employee_id"])
        return jsonify({"token": token}), 200
    return jsonify({"error": "Invalid QR code"}), 401

@app.route("/bookings", methods=["GET"])
def get_bookings():
    # Ideally, use JWT to filter employee_id
    employee_id = request.headers.get("X-Employee-ID")
    if employee_id:
        filtered = [b for b in BOOKINGS if str(b["employee_id"]) == str(employee_id)]
        return jsonify(filtered)
    return jsonify(BOOKINGS)

@app.route("/checkout", methods=["POST"])
def checkout_booking():
    data = request.get_json()
    new_booking = {
        "booking_id": len(BOOKINGS) + 1,
        "equipment_id": data["equipment_id"],
        "employee_id": data["employee_id"],
        "admin_id": data["admin_id"],
        "checkout_date": datetime.now(timezone.utc).isoformat(),
        "due_date": data["due_date"],
        "quantity_booked": data["quantity_booked"],
        "status": "CHECKED_OUT",
        "notes": data.get("notes", ""),
        "qr_code": f"BK-{len(BOOKINGS)+1}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
    }
    BOOKINGS.append(new_booking)
    return jsonify(new_booking), 201

@app.route("/checkin", methods=["PUT"])
def checkin_booking():
    data = request.get_json()
    booking_id = data.get("booking_id")
    booking = next((b for b in BOOKINGS if b["booking_id"] == booking_id), None)
    if booking:
        booking["status"] = "RETURNED"
        return jsonify(booking), 200
    return jsonify({"error": "Booking not found"}), 404

@app.route("/generate_qr", methods=["POST"])
def generate_qr():
    data = request.get_json()
    value = data.get("value")
    img_bytes = generate_qr_image(value)
    return (img_bytes, 200, {"Content-Type": "image/png"})

# -----------------------------
# Main Entry
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render provides PORT env
    app.run(host="0.0.0.0", port=port)
