# therapist_tracker/ui/add_session.py

import tkinter as tk
from tkinter import messagebox
import json
import os

DATA_FILE = "data/clients_data.json"

class AddSessionWindow(tk.Toplevel):
    def __init__(self, master, client_name):
        super().__init__(master)
        self.title(f"Add Session for {client_name}")
        self.geometry("350x300")
        self.client_name = client_name
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Date (YYYY-MM-DD):").pack(pady=5)
        self.date_entry = tk.Entry(self)
        self.date_entry.pack(pady=5)

        tk.Label(self, text="Time (e.g., 2:30 PM):").pack(pady=5)
        self.time_entry = tk.Entry(self)
        self.time_entry.pack(pady=5)

        tk.Label(self, text="Fee Charged ($):").pack(pady=5)
        self.fee_entry = tk.Entry(self)
        self.fee_entry.pack(pady=5)

        tk.Label(self, text="Paid by Client ($):").pack(pady=5)
        self.client_paid_entry = tk.Entry(self)
        self.client_paid_entry.pack(pady=5)

        tk.Label(self, text="Paid by Insurance ($):").pack(pady=5)
        self.insurance_paid_entry = tk.Entry(self)
        self.insurance_paid_entry.pack(pady=5)

        tk.Button(self, text="Save Session", command=self.save_session).pack(pady=10)

    def save_session(self):
        try:
            date = self.date_entry.get().strip()
            time = self.time_entry.get().strip()
            fee = float(self.fee_entry.get().strip())
            client_paid = float(self.client_paid_entry.get().strip())
            insurance_paid = float(self.insurance_paid_entry.get().strip())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please make sure all amounts are numbers (no text or symbols).")
            return

        if not date or not time:
            messagebox.showwarning("Missing Info", "Date and time are required.")
            return

        session = {
            "date": date,
            "time": time,
            "fee": fee,
            "client_paid": client_paid,
            "insurance_paid": insurance_paid
        }

        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
        else:
            messagebox.showerror("Error", "Client data file not found.")
            return

        for client in data:
            if client["name"] == self.client_name:
                client["sessions"].append(session)
                break
        else:
            messagebox.showerror("Error", "Client not found.")
            return

        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

        messagebox.showinfo("Saved", "Session added successfully.")
        self.destroy()
