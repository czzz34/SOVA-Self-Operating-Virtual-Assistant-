import tkinter as tk
from tkinter import messagebox
import csv
import os

CSV_FILE = "systeminfo.csv"

def get_latest_system_info():
    """
    Reads the last full record from the vertical CSV file and returns it as formatted string.
    """
    if not os.path.exists(CSV_FILE):
        return "No system information available."

    with open(CSV_FILE, "r", encoding="utf-8") as csvfile:
        reader = list(csv.reader(csvfile))
        if not reader:
            return "No system information available."

        # Group rows by blank line separator
        records = []
        current = []
        for row in reader:
            if not row or not any(row):  # blank line = new record
                if current:
                    records.append(current)
                    current = []
            else:
                current.append(row)
        if current:
            records.append(current)

        if not records:
            return "No system information available."

        latest = records[-1]
        info_str = "User Info:\n" + "\n".join([f"{key}: {value}" for key, value in latest])
        return info_str


def submit_form():
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    gender = gender_var.get().strip()
    

    # Check all fields
    if not all([name, age, gender, ]):
        messagebox.showerror("Error", "Please fill all fields.")
        return

    data = [
        ["Name", name],
        ["Age", age],
        ["Gender", gender],
       
        []
    ]

    try:
        with open(CSV_FILE, "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)
        messagebox.showinfo("Success", "System Information saved (vertically)!")
        root.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save information: {e}")


def show_system_info_form():
    """Builds and runs the system info form GUI."""
    global root, name_entry, age_entry, gender_var, cpu_entry, gpu_entry, ram_entry, screen_entry
    root = tk.Tk()
    root.title("System Info Form")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    desired_width = int(screen_width * 0.4)
    desired_height = int(screen_height * 0.65)
    root.geometry(f"{desired_width}x{desired_height}")

    def add_field(label_text):
        tk.Label(root, text=label_text, font=("Arial", 12)).pack(pady=5)
        entry = tk.Entry(root, font=("Arial", 12))
        entry.pack(pady=5)
        return entry

    name_entry = add_field("Name:")
    age_entry = add_field("Age:")

    tk.Label(root, text="Gender:", font=("Arial", 12)).pack(pady=5)
    gender_var = tk.StringVar(root)
    gender_var.set("Select Gender")
    gender_menu = tk.OptionMenu(root, gender_var, "Male", "Female", "Other")
    gender_menu.config(font=("Arial", 12))
    gender_menu.pack(pady=5)

    

    tk.Button(root, text="Submit", font=("Arial", 12), command=submit_form).pack(pady=10)
    tk.Button(root, text="Show Latest Info", font=("Arial", 12),
              command=lambda: messagebox.showinfo("Latest System Info", get_latest_system_info())).pack(pady=5)

    root.mainloop()


def run_system_info_check():
    """
    Checks if systeminfo.csv exists and has data.
    If yes, shows the info in a message box.
    If not, launches the system info form.
    """
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "r", encoding="utf-8") as csvfile:
            if any(csv.reader(csvfile)):
                info = get_latest_system_info()
                messagebox.showinfo("System Info Exists", f"System info already exists.\n\n{info}")
                return
    show_system_info_form()


if __name__ == "__main__":
    run_system_info_check()
