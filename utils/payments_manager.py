# therapist_tracker/utils/payments_manager.py

import json
import os
import uuid
from datetime import datetime
from utils.path_helper import get_resource_path

PAYMENTS_FILE = get_resource_path("data/payments.json")

def load_payments():
    if os.path.exists(PAYMENTS_FILE):
        with open(PAYMENTS_FILE, "r") as f:
            return json.load(f)
    return []

def save_payments(payments):
    with open(PAYMENTS_FILE, "w") as f:
        json.dump(payments, f, indent=4)

def add_payment(client_id, session_date, amount, payer, method="manual"):
    payments = load_payments()
    payment = {
        "payment_id": str(uuid.uuid4()),
        "client_id": client_id,
        "session_date": session_date,
        "amount": amount,
        "payer": payer,
        "method": method,
        "timestamp": datetime.now().isoformat()
    }
    payments.append(payment)
    save_payments(payments)
    return payment
