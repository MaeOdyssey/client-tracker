import tkinter as tk
from tkinter import messagebox
import json
import os

DATA_FILE = "data/clients_data.json"

class EditSessionWindow(tk.Toplevel):
    def __init__(self, parent, client_id, session_index):
        super().__init__(parent)
        self.client_id = client_id
        self.session_index = session_index
        self.session_data = self.load_session()
        self.geometry("350x300")
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
        self.date_entry = self.make_labeled_entry("Date (YYYY-MM-DD):", self.session_data.get("date", ""))
        self.time_entry = self.make_labeled_entry("Time (e.g., 2:30 PM):", self.session_data.get("time", ""))
        self.fee_entry = self.make_labeled_entry("Fee Charged ($):", self.session_data.get("fee", ""))
        self.client_paid_entry = self.make_labeled_entry("Paid by Client ($):", self.session_data.get("client_paid", ""))
        self.insurance_paid_entry = self.make_labeled_entry("Paid by Insurance ($):", self.session_data.get("insurance_paid", ""))

        tk.Button(self, text="Save Changes", command=self.save_session).pack(pady=10)

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
                "client_paid": float(self.client_paid_entry.get().strip()),
                "insurance_paid": float(self.insurance_paid_entry.get().strip())
            }
        except ValueError:
            messagebox.showerror("Invalid Input", "Please make sure all amounts are numbers.")
            return

        with open(DATA_FILE, "r") as f:
            data = json.load(f)

        for client in data:
            if client.get("client_id") == self.client_id:
                client["sessions"][self.session_index] = updated_session
                break

        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

        messagebox.showinfo("Updated", "Session updated successfully.")
        self.destroy()
