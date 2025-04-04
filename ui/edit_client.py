# therapist_tracker/ui/edit_client.py

import tkinter as tk
from tkinter import messagebox
import json
from utils.path_helper import get_resource_path

DATA_FILE = get_resource_path("data/clients_data.json")

class EditClientWindow(tk.Toplevel):
    def __init__(self, master, client_data):
        super().__init__(master)
        self.title("Edit Client Info")
        self.geometry("300x250")
        self.client_data = client_data
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Client Name:").pack(pady=5)
        self.name_entry = tk.Entry(self, width=30)
        self.name_entry.insert(0, self.client_data.get("name", ""))
        self.name_entry.pack(pady=5)

        tk.Label(self, text="Email:").pack(pady=5)
        self.email_entry = tk.Entry(self, width=30)
        self.email_entry.insert(0, self.client_data.get("email", ""))
        self.email_entry.pack(pady=5)

        tk.Label(self, text="Phone Number:").pack(pady=5)
        self.phone_entry = tk.Entry(self, width=30)
        self.phone_entry.insert(0, self.client_data.get("phone", ""))
        self.phone_entry.pack(pady=5)

        tk.Button(self, text="Save Changes", command=self.save_changes).pack(pady=10)

    def save_changes(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()

        if not name:
            messagebox.showwarning("Missing Info", "Client name cannot be empty.")
            return

        with open(DATA_FILE, "r") as f:
            data = json.load(f)

        for client in data:
            if client["client_id"] == self.client_data["client_id"]:
                client["name"] = name
                client["email"] = email
                client["phone"] = phone
                break

        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

        messagebox.showinfo("Updated", "Client info updated.")
        self.destroy()
