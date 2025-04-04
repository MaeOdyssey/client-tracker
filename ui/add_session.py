import tkinter as tk
from tkcalendar import DateEntry
from tkinter import messagebox, ttk
import json
import os
import uuid

from utils.path_helper import get_resource_path
from utils.payments_helper import create_payment

DATA_FILE = get_resource_path("data/clients_data.json")

class AddSessionWindow(tk.Toplevel):
    def __init__(self, master, client_id):
        super().__init__(master)
        self.client_id = client_id
        self.title("Add Session")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Select Date:").pack(pady=5)
        self.date_entry = DateEntry(self, date_pattern='yyyy-mm-dd', width=18)
        self.date_entry.pack(pady=5)

        tk.Label(self, text="Select Time:").pack(pady=5)
        time_options = []
        for hour in range(8, 21):
            for minute in (0, 15, 30, 45):
                suffix = "AM" if hour < 12 else "PM"
                display_hour = hour if hour <= 12 else hour - 12
                time_options.append(f"{display_hour}:{minute:02d} {suffix}")

        self.time_entry = ttk.Combobox(self, values=time_options, width=20)
        self.time_entry.set("2:00 PM")
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

        self.update_idletasks()
        self.geometry("")

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

        session_id = str(uuid.uuid4())

        session = {
            "session_id": session_id,
            "date": date,
            "time": time,
            "fee": fee
        }

        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
        else:
            messagebox.showerror("Error", "Client data file not found.")
            return

        for client in data:
            if client.get("client_id") == self.client_id:
                client["sessions"].append(session)
                break
        else:
            messagebox.showerror("Error", "Client not found.")
            return

        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

        create_payment(self.client_id, session_id, client_paid, insurance_paid)

        messagebox.showinfo("Saved", "Session and payment added successfully.")
        self.destroy()
