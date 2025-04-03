import tkinter as tk
from tkcalendar import DateEntry
from tkinter import messagebox
from tkinter import ttk
import json
import os

DATA_FILE = "data/clients_data.json"

class AddSessionWindow(tk.Toplevel):
    def __init__(self, master, client_id):
        super().__init__(master)
        self.client_id = client_id
        self.title("Add Session")
        self.create_widgets()

    def create_widgets(self):
        # 🗓️ Date picker
        tk.Label(self, text="Select Date:").pack(pady=5)
        self.date_entry = DateEntry(self, date_pattern='yyyy-mm-dd', width=18)
        self.date_entry.pack(pady=5)

        # 🕒 Time picker (15-minute intervals from 8:00 AM to 8:00 PM)
        tk.Label(self, text="Select Time:").pack(pady=5)
        time_options = []
        for hour in range(8, 21):
            for minute in (0, 15, 30, 45):
                suffix = "AM" if hour < 12 else "PM"
                display_hour = hour if hour <= 12 else hour - 12
                time_options.append(f"{display_hour}:{minute:02d} {suffix}")

        self.time_entry = ttk.Combobox(self, values=time_options, width=20)
        self.time_entry.set("2:00 PM")  # Optional default
        self.time_entry.pack(pady=5)

        # 💰 Session details
        tk.Label(self, text="Fee Charged ($):").pack(pady=5)
        self.fee_entry = tk.Entry(self)
        self.fee_entry.pack(pady=5)

        tk.Label(self, text="Paid by Client ($):").pack(pady=5)
        self.client_paid_entry = tk.Entry(self)
        self.client_paid_entry.pack(pady=5)

        tk.Label(self, text="Paid by Insurance ($):").pack(pady=5)
        self.insurance_paid_entry = tk.Entry(self)
        self.insurance_paid_entry.pack(pady=5)

        # 💾 Save button
        tk.Button(self, text="Save Session", command=self.save_session).pack(pady=10)

        # 🔄 Resize based on content
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
            if client.get("client_id") == self.client_id:
                client["sessions"].append(session)
                break
        else:
            messagebox.showerror("Error", "Client not found.")
            return

        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

        messagebox.showinfo("Saved", "Session added successfully.")
        self.destroy()
