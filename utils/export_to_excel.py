# therapist_tracker/utils/export_to_excel.py

import json
import os

from openpyxl import Workbook
from openpyxl.styles import PatternFill
from datetime import datetime
import uuid
from utils.path_helper import get_resource_path


DATA_FILE = get_resource_path("data/clients_data.json")


# Define fills for conditional formatting
PAID_FILL = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")   # soft green
UNPAID_FILL = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid") # soft red

def export_to_excel():
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError("Client data file not found.")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    uid = uuid.uuid4().hex[:5].upper()
    export_file = f"backup/theracord_backup_{timestamp}_{uid}.xlsx"

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    wb = Workbook()
    ws = wb.active
    ws.title = "Client Sessions"

    # Header row
    headers = [
        "Client Name",
        "Session Date",
        "Session Time",
        "Fee Charged",
        "Paid by Client",
        "Paid by Insurance",
        "Remaining Balance"
    ]
    ws.append(headers)

    for client in data:
        name = client["name"]
        for session in client.get("sessions", []):
            fee = session.get("fee", 0)
            client_paid = session.get("client_paid", 0)
            insurance_paid = session.get("insurance_paid", 0)
            total_paid = client_paid + insurance_paid
            remaining = fee - total_paid

            row_data = [
                name,
                session.get("date", ""),
                session.get("time", ""),
                f"${fee:.2f}",
                f"${client_paid:.2f}",
                f"${insurance_paid:.2f}",
                f"${remaining:.2f}"
            ]

            row = ws.max_row + 1
            ws.append(row_data)

            # Apply color coding
            fill = PAID_FILL if remaining <= 0 else UNPAID_FILL
            for col in range(1, 8):  # columns A-G
                ws.cell(row=row, column=col).fill = fill

        # Create backup folder if needed
        os.makedirs(os.path.dirname(export_file), exist_ok=True)

        wb.save(export_file)
        wb.close()  # This releases the file from memory
        del wb      # Optional: clears from memory to avoid lingering reference

        return export_file

