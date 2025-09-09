# python_files/apex.py
import requests
import qrcode
from datetime import datetime

BASE_URL = "https://oracleapex.com/ords/mrelokusa"
TIMEOUT = 10  # seconds

# -----------------------------
# Authentication
# -----------------------------
def login_employee(employee_code: str, password: str) -> str:
    """Login with employee_code and password; returns JWT token"""
    url = f"{BASE_URL}/employee/login"
    payload = {"employee_code": employee_code, "password": password}
    try:
        r = requests.post(url, json=payload, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()["token"]
    except requests.exceptions.Timeout:
        raise RuntimeError("APEX server timed out")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"APEX request failed: {e}")
    except KeyError:
        raise RuntimeError("APEX response missing token")

def login_employee_qr(qr_code: str) -> str:
    """Login via QR code; returns JWT token"""
    url = f"{BASE_URL}/employee/login/qr"
    payload = {"qr_code": qr_code}
    try:
        r = requests.post(url, json=payload, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()["token"]
    except requests.exceptions.Timeout:
        raise RuntimeError("APEX server timed out")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"APEX request failed: {e}")
    except KeyError:
        raise RuntimeError("APEX response missing token")

# -----------------------------
# Bookings
# -----------------------------
def get_bookings() -> list:
    url = f"{BASE_URL}/employee/bookings/active"
    try:
        r = requests.get(url, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.Timeout:
        raise RuntimeError("APEX server timed out")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"APEX request failed: {e}")

def checkout_booking(employee_id, equipment_id, quantity, due_date, admin_id, notes):
    url = f"{BASE_URL}/admin/checkout"
    payload = {
        "employee_id": employee_id,
        "equipment_id": equipment_id,
        "quantity_booked": quantity,
        "due_date": due_date,
        "admin_id": admin_id,
        "notes": notes
    }
    try:
        r = requests.post(url, json=payload, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.Timeout:
        raise RuntimeError("APEX server timed out")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"APEX request failed: {e}")

def checkin_booking(booking_id):
    url = f"{BASE_URL}/employee/checkin"
    payload = {"booking_id": booking_id}
    try:
        r = requests.put(url, json=payload, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.Timeout:
        raise RuntimeError("APEX server timed out")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"APEX request failed: {e}")

# -----------------------------
# QR Code Generation
# -----------------------------
def save_qr_image(value: str, filename: str) -> str:
    img = qrcode.make(value)
    path = f"{filename}.png"
    img.save(path)
    return path
