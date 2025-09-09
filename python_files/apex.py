Flask
import requests

APEX_BASE_URL = "https://your-apex-server.com/ords/mrelokusa"  # replace with your actual APEX base URL

def login_employee(employee_code: str, password: str) -> str:
    url = f"{APEX_BASE_URL}/employee/login"
    payload = {"EMPLOYEE_CODE": employee_code, "PASSWORD": password}
    r = requests.post(url, json=payload)
    r.raise_for_status()
    return r.json().get("token")

def login_employee_qr(qr_code: str) -> str:
    url = f"{APEX_BASE_URL}/employee/qr_login"
    payload = {"QR_CODE": qr_code}
    r = requests.post(url, json=payload)
    r.raise_for_status()
    return r.json().get("token")

def get_bookings(token: str):
    url = f"{APEX_BASE_URL}/bookings"
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()

def checkout_booking(token: str, booking_id: int):
    url = f"{APEX_BASE_URL}/bookings/{booking_id}/checkout"
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(url, headers=headers)
    r.raise_for_status()
    return r.json()
