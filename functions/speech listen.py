import threading
import tkinter as tk
import keyboard  
from functions.chatbot.ui_manager import UIManager

# Instantiate and set up the UI
ui = UIManager()
ui.root = tk.Tk()
ui.setup_ui()

# Define a listener that calls UIManager.start_listening
def listen_for_hotkey():
    # 'num 0' is the NumPad-0 key name in the `keyboard` module
    keyboard.add_hotkey('num 0', lambda: ui.start_listening())
    # Block forever, listening for events
    keyboard.wait()

# Run the hotkey listener in a daemon thread
listener_thread = threading.Thread(target=listen_for_hotkey, daemon=True)
listener_thread.start()

# Start the Tkinter main loop
ui.root.mainloop()