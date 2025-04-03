# therapist_tracker/utils/restore_from_excel.py

import os
import json
from openpyxl import load_workbook
from utils.path_helper import get_resource_path


BACKUP_FILE = get_resource_path("backup/theracord_backup.xlsx")
DATA_FILE = get_resource_path("data/clients_data.json")

def restore_from_excel():
    if not os.path.exists(BACKUP_FILE):
        raise FileNotFoundError("No backup file found.")

    wb = load_workbook(BACKUP_FILE)
    ws = wb.active

    restored_data = {}
    for row in ws.iter_rows(min_row=2, values_only=True):  # skip header
        name, date, time, fee, client_paid, insurance_paid, _ = row
        fee = float(str(fee).replace("$", ""))
        client_paid = float(str(client_paid).replace("$", ""))
        insurance_paid = float(str(insurance_paid).replace("$", ""))
        
        if name not in restored_data:
            restored_data[name] = {
                "name": name,
                "client_id": f"restored-{len(restored_data)}",
                "sessions": []
            }

        restored_data[name]["sessions"].append({
            "date": date,
            "time": time,
            "fee": fee,
            "client_paid": client_paid,
            "insurance_paid": insurance_paid
        })

    # Convert to list format
    final_data = list(restored_data.values())

    # Write back to JSON
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(final_data, f, indent=4)

    return DATA_FILE
