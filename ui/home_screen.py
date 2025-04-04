# therapist_tracker/ui/home_screen.py

import os
import platform
import subprocess
import tkinter as tk
from tkinter import messagebox

from ui.add_client import AddClientWindow
from ui.view_clients import ViewClientsWindow
from ui.unpaid_clients import UnpaidClientsWindow
from ui.add_session_picker import AddSessionClientPicker
from utils.export_to_excel import export_to_excel
from utils.restore_from_excel import restore_from_excel
from utils.path_helper import get_resource_path


class HomeScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(padx=30, pady=30)
        self.create_widgets()

    def create_widgets(self):
        # 🏷️ Title
        tk.Label(self, text="Theracord", font=("Helvetica", 18, "bold")).pack(pady=(0, 20))

        # 📂 Session Tools
        session_frame = tk.LabelFrame(self, text="Session Tools", padx=10, pady=10, font=("Helvetica", 12, "bold"))
        session_frame.pack(pady=10, fill="x")
        tk.Button(session_frame, text="Add Session", width=30, command=self.open_add_session).pack(pady=5)
        tk.Button(session_frame, text="View Sessions", width=30, command=self.open_view_clients).pack(pady=5)
        tk.Button(session_frame, text="Unpaid Balances", width=30, command=self.open_unpaid_clients).pack(pady=5)

        # 👥 Client Tools
        client_frame = tk.LabelFrame(self, text="Client Tools", padx=10, pady=10, font=("Helvetica", 12, "bold"))
        client_frame.pack(pady=10, fill="x")
        tk.Button(client_frame, text="Add New Client", width=30, command=self.open_add_client).pack(pady=5)
        tk.Button(client_frame, text="View Clients", width=30, command=self.open_view_clients).pack(pady=5)

        # 📦 Backup Tools
        backup_frame = tk.LabelFrame(self, text="Backup", padx=10, pady=10, font=("Helvetica", 12, "bold"))
        backup_frame.pack(pady=10, fill="x")
        tk.Button(backup_frame, text="Create Backup (Excel)", width=30, command=self.handle_export).pack(pady=5)
        tk.Button(backup_frame, text="Restore from Backup", width=30, command=self.handle_restore).pack(pady=5)
        tk.Button(backup_frame, text="Open Backup Folder", width=30, command=self.open_backup_folder).pack(pady=5)

    # 👤 Client actions
    def open_add_client(self):
        AddClientWindow(self.master)

    def open_view_clients(self):
        ViewClientsWindow(self.master)

    def open_unpaid_clients(self):
        UnpaidClientsWindow(self.master)

    def open_add_session(self):
        AddSessionClientPicker(self.master)

    # 💾 Export / Restore
    def handle_export(self):
        try:
            filepath = export_to_excel()
            messagebox.showinfo("Export Successful", f"Data saved to:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Export Failed", str(e))

    def handle_restore(self):
        result = messagebox.askyesno("Confirm Restore", "Restoring will overwrite current data. Continue?")
        if result:
            try:
                restore_from_excel()
                messagebox.showinfo("Restore Complete", "Data has been restored from backup.")
            except Exception as e:
                messagebox.showerror("Restore Failed", str(e))

    def open_backup_folder(self):
        backup_path = get_resource_path("backup")
        if not os.path.exists(backup_path):
            messagebox.showwarning("No Backups", "No backup folder found yet.")
            return

        if platform.system() == "Windows":
            os.startfile(backup_path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.Popen(["open", backup_path])
        else:  # Linux and others
            subprocess.Popen(["xdg-open", backup_path])
