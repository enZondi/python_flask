# python_files/apex_api.py
from flask import Flask, request, jsonify
import requests
import apex  # your apex.py module

app = Flask(__name__)
apex_client = apex  # your existing apex.py functions

@app.route("/login", methods=["POST"])
def login():
    """Employee login via APEX REST API"""
    data = request.json
    try:
        token = apex_client.login_employee(data["employee_code"], data["password"])
        return jsonify({"token": token})
    except requests.exceptions.RequestException as e:
        # Catch HTTP errors from APEX
        return jsonify({"error": str(e)}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/login/qr", methods=["POST"])
def login_qr():
    """Employee login via QR code"""
    data = request.json
    try:
        token = apex_client.login_employee_qr(data["qr_code"])
        return jsonify({"token": token})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/bookings", methods=["GET"])
def get_bookings():
    """Fetch bookings via APEX REST API"""
    try:
        bookings = apex_client.get_bookings()
        return jsonify(bookings)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/checkout", methods=["POST"])
def checkout_booking():
    """Admin checkout booking via APEX REST API"""
    data = request.json
    try:
        result = apex_client.checkout_booking(
            data["employee_id"],
            data["equipment_id"],
            data["quantity"],
            data["due_date"],
            data["admin_id"],
            data.get("notes", "")
        )
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/checkin", methods=["PUT"])
def checkin_booking():
    """Employee checkin booking via APEX REST API"""
    data = request.json
    try:
        result = apex_client.checkin_booking(data["booking_id"])
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Optional health check
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    # Render expects this to bind on 0.0.0.0:$PORT
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
