# therapist_tracker/ui/add_client.py

import tkinter as tk
import json
import os
import uuid
from tkinter import messagebox
from ui.add_session import AddSessionWindow
from utils.path_helper import get_resource_path


DATA_FILE = get_resource_path("data/clients_data.json")

class AddClientWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Add New Client")
        self.geometry("")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Client Name:", font=("Helvetica", 10, "bold")).pack(pady=5)
        self.name_entry = tk.Entry(self, width=30)
        self.name_entry.pack(pady=5)

        tk.Label(self, text="Email (optional):").pack(pady=5)
        self.email_entry = tk.Entry(self, width=30)
        self.email_entry.pack(pady=5)

        tk.Label(self, text="Phone Number:").pack(pady=5)
        self.phone_entry = tk.Entry(self, width=30)
        self.phone_entry.pack(pady=5)

        tk.Button(self, text="Save", command=self.save_client).pack(pady=10)

    def save_client(self):
        phone = self.phone_entry.get().strip()
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        if not name:
            messagebox.showwarning("Missing Info", "Client name cannot be empty.")
            return
        new_client = {
            "client_id": str(uuid.uuid4()),
            "name": name,
            "email": email, 
            "phone": phone,

            "sessions": []
        }

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

        response = messagebox.askyesno(
            "Client Added",
            f"Client '{name}' added successfully.\n\nWould you like to add a session now?"
        )

        self.destroy()  # Close this window before doing anything else

        if response:
            AddSessionWindow(self.master, client_id=new_client["client_id"])
        else:
            messagebox.showinfo("Done", "Client saved.")
