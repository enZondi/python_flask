# python_files/apex.py

import requests
import qrcode
import io
import base64
from datetime import datetime, timezone

# -----------------------------
# Config: Oracle APEX REST endpoints
# -----------------------------
BASE_URL = "https://oracleapex.com/ords/mrelokusa"

# -----------------------------
# Authentication
# -----------------------------
def login_employee(employee_code: str, password: str) -> str:
    """Login with employee_code and password; returns JWT token"""
    url = f"{BASE_URL}/employee/login"
    payload = {"employee_code": employee_code, "password": password}
    r = requests.post(url, json=payload)
    r.raise_for_status()
    data = r.json()
    return data["token"]

def login_employee_qr(qr_code: str) -> str:
    """Login via QR code; returns JWT token"""
    url = f"{BASE_URL}/employee/login/qr"
    payload = {"qr_code": qr_code}
    r = requests.post(url, json=payload)
    r.raise_for_status()
    data = r.json()
    return data["token"]

# -----------------------------
# Bookings
# -----------------------------
def get_bookings() -> list:
    """Fetch bookings (filtered by employee in APEX)"""
    url = f"{BASE_URL}/employee/bookings/active"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

def checkout_booking(employee_id, equipment_id, quantity, due_date, admin_id, notes):
    """Admin creates a new booking"""
    url = f"{BASE_URL}/admin/checkout"
    payload = {
        "employee_id": employee_id,
        "equipment_id": equipment_id,
        "quantity_booked": quantity,
        "due_date": due_date,
        "admin_id": admin_id,
        "notes": notes
    }
    r = requests.post(url, json=payload)
    r.raise_for_status()
    return r.json()

def checkin_booking(booking_id):
    """Employee checks in a booking"""
    url = f"{BASE_URL}/employee/checkin"
    payload = {"booking_id": booking_id}
    r = requests.put(url, json=payload)
    r.raise_for_status()
    return r.json()

# -----------------------------
# QR Code Generation
# -----------------------------
def save_qr_image(value: str, filename: str) -> str:
    """Generate QR code PNG and save locally"""
    img = qrcode.make(value)
    path = f"{filename}.png"
    img.save(path)
    return path
