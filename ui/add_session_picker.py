import tkinter as tk
from tkinter import messagebox
import json
import os
from ui.add_session import AddSessionWindow
from utils.path_helper import get_resource_path


DATA_FILE = get_resource_path("data/clients_data.json")

class AddSessionClientPicker(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Select Client")
        self.geometry("300x250")
        self.clients = self.load_clients()
        self.create_widgets()

    def load_clients(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        return []

    def create_widgets(self):
        tk.Label(self, text="Choose a Client:").pack(pady=5)

        height = min(len(self.clients), 10) or 5
        self.client_listbox = tk.Listbox(self, width=35, height=height)
        self.client_listbox.pack(pady=5)

        for client in self.clients:
            name = client["name"].strip()
            email = client.get("email", "No email").strip()
            display_text = f"{name} ({email})"

            self.client_listbox.insert(tk.END, display_text)

        tk.Button(self, text="Select", command=self.select_client).pack(pady=10)

    def select_client(self):
        index = self.client_listbox.curselection()
        if not index:
            messagebox.showwarning("Select Client", "Please select a client.")
            return

        selected = self.clients[index[0]]
        self.destroy()
        AddSessionWindow(self.master, client_id=selected["client_id"])
