# therapist_tracker/main.py

import tkinter as tk
from ui.home_screen import HomeScreen

def main():
    root = tk.Tk()
    root.title("Therapist Client Tracker")
    app = HomeScreen(root)
    root.mainloop()

if __name__ == "__main__":
    main()
