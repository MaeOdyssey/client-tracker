import tkinter as tk
from tkinter import messagebox
import json
import os
import uuid

from ui.edit_session import EditSessionWindow
from ui.add_session import AddSessionWindow
from utils.path_helper import get_resource_path


DATA_FILE = get_resource_path( "data/clients_data.json")

class ViewClientsWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("View Clients and Sessions")
        self.geometry("600x450")
        self.clients = self.load_clients()
        self.selected_client = None
        self.selected_client_id = None
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
                data = json.load(f)

            # Patch missing client_ids
            updated = False
            for client in data:
                if "client_id" not in client:
                    client["client_id"] = str(uuid.uuid4())
                    updated = True

            if updated:
                with open(DATA_FILE, "w") as f:
                    json.dump(data, f, indent=4)

            return data
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
        self.selected_client_id = self.selected_client["client_id"]
        self.show_sessions()

    def show_sessions(self):
        for widget in self.session_frame.winfo_children():
            widget.destroy()

        tk.Label(self.session_frame, text=f"Sessions for {self.selected_client['name']}:", font=("Helvetica", 12)).pack()

        if not self.selected_client["sessions"]:
            tk.Label(self.session_frame, text="No sessions recorded.").pack(pady=5)

            button_frame = tk.Frame(self.session_frame)
            button_frame.pack(pady=10)

            tk.Button(button_frame, text="➕ Add Session", command=self.add_session_for_client).pack(side="left", padx=5)
            tk.Button(button_frame, text="🗑️ Delete Client", command=self.delete_client).pack(side="left", padx=5)
            return

        self.session_listbox = tk.Listbox(self.session_frame, height=8, width=60)
        self.session_listbox.pack(pady=5)
        self.session_listbox.bind("<<ListboxSelect>>", self.display_session_details)

        for i, session in enumerate(self.selected_client["sessions"]):
            self.session_listbox.insert(tk.END, f"{i + 1}. {session['date']} @ {session['time']}")

        self.session_detail_frame = tk.Frame(self.session_frame)
        self.session_detail_frame.pack(fill="x", pady=10)
        self.update_idletasks()
        self.geometry("")

    def display_session_details(self, event):
        for widget in self.session_detail_frame.winfo_children():
            widget.destroy()

        selection = self.session_listbox.curselection()
        if not selection:
            return

        index = selection[0]
        session = self.selected_client["sessions"][index]

        remaining = session["fee"] - (session["client_paid"] + session["insurance_paid"])
        status = f"Remaining: ${remaining:.2f}" if remaining > 0 else "Fully paid ✅"

        detail_text = (
            f"📅 Date: {session['date']}\n"
            f"🕒 Time: {session['time']}\n"
            f"💰 Fee: ${session['fee']:.2f}\n"
            f"👤 Client Paid: ${session['client_paid']:.2f}\n"
            f"🏥 Insurance Paid: ${session['insurance_paid']:.2f}\n"
            f"📌 {status}"
        )

        tk.Label(self.session_detail_frame, text=detail_text, justify="left", anchor="w", font=("Helvetica", 10)).pack(padx=10, pady=5)

        button_frame = tk.Frame(self.session_detail_frame)
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="Edit Session", width=15, command=lambda: self.edit_session(index)).pack(side="left", padx=5)
        tk.Button(button_frame, text="Delete Session", width=15, command=lambda: self.delete_session(index)).pack(side="left", padx=5)
        self.update_idletasks()
        self.geometry("")

    def edit_session(self, session_index):
        EditSessionWindow(self, client_id=self.selected_client_id, session_index=session_index)

    def delete_session(self, session_index):
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this session?")
        if not confirm:
            return

        with open(DATA_FILE, "r") as f:
            data = json.load(f)

        for client in data:
            if client["client_id"] == self.selected_client_id:
                try:
                    del client["sessions"][session_index]
                except IndexError:
                    messagebox.showerror("Error", "Session not found.")
                    return
                break

        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

        messagebox.showinfo("Deleted", "Session removed.")
        self.selected_client["sessions"].pop(session_index)
        self.show_sessions()

    def add_session_for_client(self):
        AddSessionWindow(self, client_id=self.selected_client_id)

    def delete_client(self):
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {self.selected_client['name']}?")
        if not confirm:
            return

        with open(DATA_FILE, "r") as f:
            data = json.load(f)

        # Remove client by ID
        data = [client for client in data if client.get("client_id") != self.selected_client_id]

        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

        messagebox.showinfo("Deleted", "Client deleted successfully.")

        # Refresh client list
        self.clients = data
        self.selected_client = None
        self.selected_client_id = None

        # Clear listbox & repopulate
        self.client_listbox.delete(0, tk.END)
        for client in self.clients:
            self.client_listbox.insert(tk.END, client["name"])

        # Clear session frame
        for widget in self.session_frame.winfo_children():
            widget.destroy()
