# therapist_tracker/main.py

import tkinter as tk
import sys
import os 
from ui.home_screen import HomeScreen


def main():
    root = tk.Tk()
    root.title("Theracord")
    app = HomeScreen(root)
    root.mainloop()

if __name__ == "__main__":
    main()
