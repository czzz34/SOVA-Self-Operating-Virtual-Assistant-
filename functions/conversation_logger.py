import csv
import os
from datetime import datetime
from functions.systeminfo_form import get_latest_system_info

user_system_info = get_latest_system_info()

prompt = (
    "You are a sophisticated AI assistant that personalizes responses based on the user's system information. "
    "Here is the user's system information:\n\n"
    f"{user_system_info}\n\n"
    "Now, please respond to the user's query accordingly."
)


CSV_PATH = "chat.csv"

def init_chat_csv(csv_path=CSV_PATH):
    """Initializes the CSV file with headers if it does not exist."""
    if not os.path.exists(csv_path):
        with open(csv_path, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Sender", "Message"])

def log_message(sender: str, message: str, csv_path=CSV_PATH):
    """Appends a new conversation row to the CSV file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(csv_path, "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, sender, message])
