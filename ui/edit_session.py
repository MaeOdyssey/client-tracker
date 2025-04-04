import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import json
import uuid
from utils.path_helper import get_resource_path
from utils.payments_helper import (
    get_payment_by_session_id,
    update_payment
)

DATA_FILE = get_resource_path("data/clients_data.json")

class EditSessionWindow(tk.Toplevel):
    def __init__(self, parent, client_id, session_index):
        super().__init__(parent)
        self.client_id = client_id
        self.session_index = session_index
        self.session_data = self.load_session()
        self.session_id = self.session_data.get("session_id")
        self.payment_data = get_payment_by_session_id(self.session_id)

        self.geometry("350x400")
        self.title("Edit Session")
        self.create_widgets()

    def load_session(self):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        for client in data:
            if client.get("client_id") == self.client_id:
                return client["sessions"][self.session_index]
        return {}

    def create_widgets(self):
        # 🗓️ Date picker
        tk.Label(self, text="Select Date:").pack(pady=5)
        self.date_entry = DateEntry(self, date_pattern='yyyy-mm-dd', width=18)
        self.date_entry.set_date(self.session_data.get("date", ""))
        self.date_entry.pack(pady=5)

        # 🕒 Time picker
        tk.Label(self, text="Select Time:").pack(pady=5)
        time_options = []
        for hour in range(8, 21):
            for minute in (0, 15, 30, 45):
                suffix = "AM" if hour < 12 else "PM"
                display_hour = hour if hour <= 12 else hour - 12
                time_options.append(f"{display_hour}:{minute:02d} {suffix}")
        self.time_entry = ttk.Combobox(self, values=time_options, width=20)
        self.time_entry.set(self.session_data.get("time", "2:00 PM"))
        self.time_entry.pack(pady=5)

        # 💰 Financial fields
        self.fee_entry = self.make_labeled_entry("Fee Charged ($):", self.session_data.get("fee", ""))

        paid_by_client = self.payment_data.get("client_paid", "") if self.payment_data else ""
        paid_by_insurance = self.payment_data.get("insurance_paid", "") if self.payment_data else ""
        self.client_paid_entry = self.make_labeled_entry("Paid by Client ($):", paid_by_client)
        self.insurance_paid_entry = self.make_labeled_entry("Paid by Insurance ($):", paid_by_insurance)

        tk.Button(self, text="Save Changes", command=self.save_session).pack(pady=10)

        self.update_idletasks()
        self.geometry("")

    def make_labeled_entry(self, label_text, initial_value):
        tk.Label(self, text=label_text).pack(pady=2)
        entry = tk.Entry(self)
        entry.pack()
        entry.insert(0, str(initial_value))
        return entry

    def save_session(self):
        try:
            updated_session = {
                "date": self.date_entry.get().strip(),
                "time": self.time_entry.get().strip(),
                "fee": float(self.fee_entry.get().strip()),
                "session_id": self.session_id  # Keep session ID
            }

            updated_payment_data = {
                "client_paid": float(self.client_paid_entry.get().strip()),
                "insurance_paid": float(self.insurance_paid_entry.get().strip())
            }

        except ValueError:
            messagebox.showerror("Invalid Input", "Please make sure all amounts are numbers.")
            return

        # Update session in JSON
        with open(DATA_FILE, "r") as f:
            data = json.load(f)

        for client in data:
            if client.get("client_id") == self.client_id:
                client["sessions"][self.session_index] = updated_session
                break

        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

        # Update corresponding payment
        update_payment(self.session_id, updated_payment_data)

        messagebox.showinfo("Updated", "Session and payment updated successfully.")
        self.destroy()
