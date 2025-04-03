import tkinter as tk
from tkinter import messagebox
import json
import os

DATA_FILE = "data/clients_data.json"

class ViewClientsWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("View Clients and Sessions")
        self.geometry("500x400")
        self.clients = self.load_clients()
        self.selected_client = None
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Select a Client:").pack(pady=5)

        self.client_listbox = tk.Listbox(self, width=50, height=10)
        self.client_listbox.pack(pady=5)
        self.client_listbox.bind("<<ListboxSelect>>", self.on_client_select)

        for client in self.clients:
            self.client_listbox.insert(tk.END, client["name"])

        self.session_frame = tk.Frame(self)
        self.session_frame.pack(fill="both", expand=True, pady=10)

    def load_clients(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        else:
            messagebox.showerror("Error", "Client data file not found.")
            self.destroy()
            return []

    def on_client_select(self, event):
        selection = self.client_listbox.curselection()
        if not selection:
            return

        index = selection[0]
        self.selected_client = self.clients[index]
        self.show_sessions()

    def show_sessions(self):
        for widget in self.session_frame.winfo_children():
            widget.destroy()

        tk.Label(self.session_frame, text=f"Sessions for {self.selected_client['name']}:", font=("Helvetica", 12)).pack()

        if not self.selected_client["sessions"]:
            tk.Label(self.session_frame, text="No sessions recorded.").pack()
            return

        for idx, session in enumerate(self.selected_client["sessions"], start=1):
            text = (
                f"{idx}. Date: {session['date']} | Time: {session['time']}\n"
                f"   Fee: ${session['fee']} | Client Paid: ${session['client_paid']} | Insurance Paid: ${session['insurance_paid']}"
            )
            tk.Label(self.session_frame, text=text, justify="left", anchor="w").pack(fill="x", padx=10, pady=2)
