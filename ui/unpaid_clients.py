import tkinter as tk
from tkinter import messagebox
from ui.edit_session import EditSessionWindow
import json
import os
from utils.path_helper import get_resource_path

DATA_FILE = get_resource_path("data/clients_data.json")

class UnpaidClientsWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Clients with Outstanding Balances")
        self.geometry("600x450")

        self.clients_data = self.load_data()
        self.unpaid_clients = self.get_unpaid_clients()
        self.selected_client = None

        self.client_listbox = None
        self.session_frame = None

        self.create_widgets()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        else:
            messagebox.showerror("Error", "Client data file not found.")
            self.destroy()
            return []

    def get_unpaid_clients(self):
        unpaid = []
        for client in self.clients_data:
            for session in client.get("sessions", []):
                total_paid = session.get("client_paid", 0) + session.get("insurance_paid", 0)
                if total_paid < session.get("fee", 0):
                    unpaid.append(client)
                    break
        return unpaid

    def create_widgets(self):
        tk.Label(self, text="Clients with Unpaid Sessions:", font=("Helvetica", 12)).pack(pady=5)

        if not self.unpaid_clients:
            tk.Label(self, text="🎉 All sessions are fully paid!").pack(pady=20)
            return

        self.client_listbox = tk.Listbox(self, width=40, height=10)
        self.client_listbox.pack(pady=5)
        self.client_listbox.bind("<<ListboxSelect>>", self.on_client_select)

        for client in self.unpaid_clients:
            self.client_listbox.insert(tk.END, client["name"])

        self.session_frame = tk.Frame(self)
        self.session_frame.pack(fill="both", expand=True, pady=10)

    def on_client_select(self, event):
        for widget in self.session_frame.winfo_children():
            widget.destroy()

        index = self.client_listbox.curselection()
        if not index:
            return

        selected = self.unpaid_clients[index[0]]
        self.selected_client = selected

        tk.Label(self.session_frame, text=f"Unpaid Sessions for {selected['name']}:", font=("Helvetica", 11)).pack(pady=(5, 10))

        for i, session in enumerate(selected.get("sessions", [])):
            total_paid = session["client_paid"] + session["insurance_paid"]
            if total_paid < session["fee"]:
                remaining = session["fee"] - total_paid
                text = (
                    f"{session['date']} @ {session['time']} | "
                    f"Fee: ${session['fee']} | Paid: ${total_paid:.2f} | "
                    f"Remaining: ${remaining:.2f}"
                )

                frame = tk.Frame(self.session_frame)
                frame.pack(fill="x", padx=10, pady=4)

                tk.Label(frame, text=text, anchor="w", justify="left").pack(side="left", fill="x", expand=True)

                tk.Button(frame, text="Edit", command=lambda idx=i: self.edit_session(idx)).pack(side="right", padx=5)
    def edit_session(self, session_index):
        client_id = self.selected_client.get("client_id")
        if client_id is not None:
            EditSessionWindow(self, client_id, session_index)
            #self.destroy()   Close the unpaid window after launching editor
