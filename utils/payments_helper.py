import os
import json
import uuid
from utils.path_helper import get_resource_path

PAYMENTS_FILE = get_resource_path("data/payments.json")

def load_payments():
    if os.path.exists(PAYMENTS_FILE):
        with open(PAYMENTS_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []  # Treat empty or broken file as an empty list
    return []


def save_all_payments(payments):
    with open(PAYMENTS_FILE, "w") as f:
        json.dump(payments, f, indent=4)

def save_payment(payment_record):
    payments = load_payments()
    payments.append(payment_record)
    save_all_payments(payments)

def get_payment_by_session_id(session_id):
    payments = load_payments()
    return next((p for p in payments if p.get("session_id") == session_id), None)

def get_payments_by_client_id(client_id):
    return [p for p in load_payments() if p.get("client_id") == client_id]

def update_payment(session_id, new_data):
    payments = load_payments()
    updated = False
    for i, payment in enumerate(payments):
        if payment["session_id"] == session_id:
            payments[i].update(new_data)
            updated = True
            break
    if updated:
        save_all_payments(payments)

def delete_payment(session_id):
    payments = load_payments()
    payments = [p for p in payments if p.get("session_id") != session_id]
    save_all_payments(payments)

def get_total_paid_for_session(session_id):
    payment = get_payment_by_session_id(session_id)
    if payment:
        return payment.get("client_paid", 0) + payment.get("insurance_paid", 0)
    return 0

def create_payment(client_id, session_id, client_paid, insurance_paid):
    new_payment = {
        "payment_id": str(uuid.uuid4()),
        "client_id": client_id,
        "session_id": session_id,
        "client_paid": float(client_paid),
        "insurance_paid": float(insurance_paid)
    }
    save_payment(new_payment)
    return new_payment
