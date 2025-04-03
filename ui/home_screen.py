# therapist_tracker/ui/home_screen.py

import tkinter as tk
from ui.add_client import AddClientWindow

class HomeScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(padx=20, pady=20)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Therapist Client Tracker", font=("Helvetica", 16)).pack(pady=10)

        tk.Button(self, text="Add New Client", width=25, command=self.open_add_client).pack(pady=5)
        tk.Button(self, text="Export to Excel (Coming Soon)", state='disabled', width=25).pack(pady=5)

    def open_add_client(self):
        AddClientWindow(self.master)
