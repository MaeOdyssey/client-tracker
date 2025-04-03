# therapist_tracker/ui/home_screen.py

import tkinter as tk
from ui.add_client import AddClientWindow
from ui.add_session import AddSessionWindow
from ui.view_clients import ViewClientsWindow


class HomeScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(padx=20, pady=20)
        self.create_widgets()

    def create_widgets(self):
        tk.Button(self, text="Add Session (Test)", width=25, command=self.test_add_session).pack(pady=5)
        tk.Label(self, text="Therapist Client Tracker", font=("Helvetica", 16)).pack(pady=10)

        tk.Button(self, text="Add New Client", width=25, command=self.open_add_client).pack(pady=5)
        tk.Button(self, text="Export to Excel (Coming Soon)", state='disabled', width=25).pack(pady=5)
        tk.Button(self, text="View Clients & Sessions", width=25, command=self.open_view_clients).pack(pady=5)


    def open_add_client(self):
        AddClientWindow(self.master)
    
    def test_add_session(self):
        AddSessionWindow(self.master, client_name="John Doe")
    def open_view_clients(self):
        ViewClientsWindow(self.master)
