# therapist_tracker/ui/add_client.py

import tkinter as tk
import json
import os
from tkinter import messagebox


DATA_FILE = "data/clients_data.json"

class AddClientWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Add New Client")
        self.geometry("300x150")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Client Name:").pack(pady=5)
        self.name_entry = tk.Entry(self, width=30)
        self.name_entry.pack(pady=5)

        tk.Button(self, text="Save", command=self.save_client).pack(pady=10)

    def save_client(self):
        name = self.name_entry.get().strip()
        if not name:
            tk.messagebox.showwarning("Missing Info", "Client name cannot be empty.")
            return

        new_client = {"name": name, "sessions": []}

        # Load existing data
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
        else:
            data = []

        data.append(new_client)

        # Save updated data
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

        tk.messagebox.showinfo("Saved", f"Client '{name}' added.")
        self.destroy()
