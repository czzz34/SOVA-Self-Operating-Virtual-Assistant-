# functions/chatbot/self_training.py
import os
import time
import json
import threading
import tkinter as tk
from tkinter import messagebox, filedialog
from pynput import keyboard, mouse
import pyautogui
import os


def get_json_filenames():
    """Returns a list of JSON file names (without paths) in the 'user_training' directory."""
    base_dir = os.path.join(os.path.dirname(__file__), "user_training")
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    json_files = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.lower().endswith('.json'):
                json_files.append(file)  # Only the file name, not the full path
    return json_files

# --- Special Keys Mapping ---
special_keys = {
    "Key.space": "space",
    "Key.enter": "enter",
    "Key.shift": "shift",
    "Key.shift_r": "shift",
    "Key.ctrl": "ctrl",
    "Key.ctrl_l": "ctrl",
    "Key.ctrl_r": "ctrl",
    "Key.alt": "alt",
    "Key.alt_l": "alt",
    "Key.alt_r": "alt",
    "Key.tab": "tab",
    "Key.caps_lock": "capslock",
    "Key.delete": "delete",
    "Key.backspace": "backspace",
    "Key.insert": "insert",
    "Key.f1": "f1",
    "Key.f2": "f2",
    "Key.f3": "f3",
    "Key.f4": "f4",
    "Key.f5": "f5",
    "Key.f6": "f6",
    "Key.f7": "f7",
    "Key.f8": "f8",
    "Key.f9": "f9",
    "Key.f10": "f10",
    "Key.f11": "f11",
    "Key.f12": "f12",
    "Key.cmd": "winleft",
    "Key.cmd_l": "winleft",
    "Key.cmd_r": "winright"
}

def get_user_training_path(file_name: str) -> str:
    """
    Returns the full path for a JSON file to be stored in the 'user_training' directory.
    Creates the directory if it doesn't exist.
    """
    base_dir = os.path.dirname(__file__)
    training_dir = os.path.join(base_dir, "user_training")
    if not os.path.exists(training_dir):
        os.makedirs(training_dir)
    return os.path.join(training_dir, file_name)

class MacroRecorderPlayer:
    def __init__(self, update_status, append_log):
        self.events = []              # Recorded events
        self.start_time = None        # Recording start time
        self.key_press_times = {}     # Timestamps for key presses
        self.pressed_keys = []        # Current combination of pressed keys
        self.update_status = update_status
        self.append_log = append_log

    # --- Keyboard Event Handlers ---
    def record_keyboard_press(self, key):
        event_time = time.time() - self.start_time
        try:
            key_val = key.char if key.char is not None else str(key)
        except AttributeError:
            key_val = str(key)
        if key_val not in self.pressed_keys:
            self.pressed_keys.append(key_val)
        self.key_press_times[key] = event_time
        self.events.append({
            "type": "keyboard",
            "event": "press",
            "keys": self.pressed_keys.copy(),
            "time": event_time
        })
        if key == keyboard.Key.esc:
            # Stop recording when ESC is pressed
            return False

    def record_keyboard_release(self, key):
        event_time = time.time() - self.start_time
        try:
            key_val = key.char if key.char is not None else str(key)
        except AttributeError:
            key_val = str(key)
        self.events.append({
            "type": "keyboard",
            "event": "release",
            "keys": self.pressed_keys.copy(),
            "time": event_time
        })
        if key_val in self.pressed_keys:
            self.pressed_keys.remove(key_val)
        if key in self.key_press_times:
            self.key_press_times.pop(key)

    # --- Mouse Event Handlers ---
    def on_mouse_move(self, x, y):
        event_time = time.time() - self.start_time
        self.events.append({
            "type": "mouse",
            "event": "move",
            "position": (x, y),
            "time": event_time
        })

    def on_mouse_click(self, x, y, button, pressed):
        event_time = time.time() - self.start_time
        self.events.append({
            "type": "mouse",
            "event": "click",
            "position": (x, y),
            "button": button.name,
            "pressed": pressed,
            "time": event_time
        })

    def on_mouse_scroll(self, x, y, dx, dy):
        event_time = time.time() - self.start_time
        self.events.append({
            "type": "mouse",
            "event": "scroll",
            "position": (x, y),
            "dx": dx,
            "dy": dy,
            "time": event_time
        })

    def record_events(self, file_name):
        # Build full file path in user_training folder.
        full_file_name = get_user_training_path(file_name)
        self.events = []
        self.key_press_times = {}
        self.pressed_keys = []
        self.start_time = time.time()
        self.update_status("Recording...")
        self.append_log("Recording events... (Press ESC to stop recording)")
        kb_listener = keyboard.Listener(
            on_press=self.record_keyboard_press,
            on_release=self.record_keyboard_release
        )
        ms_listener = mouse.Listener(
            on_move=self.on_mouse_move,
            on_click=self.on_mouse_click,
            on_scroll=self.on_mouse_scroll
        )
        kb_listener.start()
        ms_listener.start()
        kb_listener.join()  # Blocks until ESC is pressed
        ms_listener.stop()
        try:
            with open(full_file_name, "w") as f:
                json.dump(self.events, f, indent=4)
        except Exception as e:
            self.append_log(f"Error saving file: {e}")
        self.update_status("Idle")
        self.append_log(f"Recording stopped. Events saved to {full_file_name}")
        messagebox.showinfo("Recording", f"Recording stopped.\nEvents saved to {full_file_name}")

    def replay_events(self, file_name):
        full_file_name = get_user_training_path(file_name)
        try:
            with open(full_file_name, "r") as f:
                events = json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {e}")
            return
        self.update_status("Replaying...")
        self.append_log(f"Replaying events from {full_file_name}")
        last_event_time = 0
        for event in events:
            delay = event["time"] - last_event_time
            time.sleep(delay)
            last_event_time = event["time"]
            if event["type"] == "keyboard":
                keys = event["keys"]
                # Map keys to pyautogui-friendly values
                mapped_keys = [special_keys.get(k, k) for k in keys]
                if event["event"] == "press":
                    if len(mapped_keys) > 1:
                        pyautogui.hotkey(*mapped_keys)
                    else:
                        pyautogui.keyDown(mapped_keys[0])
                elif event["event"] == "release":
                    if len(mapped_keys) == 1:
                        pyautogui.keyUp(mapped_keys[0])
            elif event["type"] == "mouse":
                if event["event"] == "move":
                    x, y = event["position"]
                    pyautogui.moveTo(x, y)
                elif event["event"] == "click":
                    x, y = event["position"]
                    btn = event["button"]
                    if event["pressed"]:
                        pyautogui.mouseDown(x=x, y=y, button=btn)
                    else:
                        pyautogui.mouseUp(x=x, y=y, button=btn)
                elif event["event"] == "scroll":
                    x, y = event["position"]
                    dx, dy = event["dx"], event["dy"]
                    if dy:
                        pyautogui.scroll(dy, x=x, y=y)
                    if dx:
                        pyautogui.hscroll(dx, x=x, y=y)
        self.update_status("Idle")
        self.append_log("Replay completed!")
        

class SelfTrainingWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Self Training - Macro Recorder & Player")
        self.window.minsize(600, 400)
        
        # Configure grid layout
        self.window.grid_rowconfigure(4, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        
        # File selection frame
        file_frame = tk.Frame(self.window)
        file_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        file_frame.columnconfigure(1, weight=1)
        file_label = tk.Label(file_frame, text="JSON File Name:")
        file_label.grid(row=0, column=0, padx=5, sticky="w")
        self.file_entry = tk.Entry(file_frame, width=30)
        self.file_entry.grid(row=0, column=1, padx=5, sticky="ew")
        self.file_entry.insert(0, "recorded_steps.json")
        browse_button = tk.Button(file_frame, text="Browse", command=self.browse_file, width=10)
        browse_button.grid(row=0, column=2, padx=5)
        
        # Buttons frame for Record & Replay
        button_frame = tk.Frame(self.window)
        button_frame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        button_frame.columnconfigure((0, 1), weight=1)
        self.macro = MacroRecorderPlayer(self.update_status, self.append_log)
        record_button = tk.Button(button_frame, text="Record", command=lambda: threading.Thread(
            target=self.macro.record_events,
            args=(self.get_file_name(),),
            daemon=True).start(), width=15)
        record_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        replay_button = tk.Button(button_frame, text="Replay", command=lambda: threading.Thread(
            target=self.macro.replay_events,
            args=(self.get_file_name(),),
            daemon=True).start(), width=15)
        replay_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Status label
        self.status_label = tk.Label(self.window, text="Status: Idle", fg="blue")
        self.status_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        
        # Log window
        log_label = tk.Label(self.window, text="Log:")
        log_label.grid(row=3, column=0, padx=5, pady=(10, 0), sticky="w")
        self.log_text = tk.Text(self.window, height=10)
        self.log_text.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")
        clear_log_button = tk.Button(self.window, text="Clear Log", command=self.clear_log, width=15)
        clear_log_button.grid(row=5, column=0, padx=5, pady=5, sticky="ew")
        
        # JSON Files List Frame (Auto-search)
        json_frame = tk.Frame(self.window)
        json_frame.grid(row=6, column=0, padx=5, pady=5, sticky="nsew")
        json_frame.columnconfigure(0, weight=1)
        json_label = tk.Label(json_frame, text="Available JSON Files:")
        json_label.pack(side=tk.TOP, anchor="w")
        self.json_listbox = tk.Listbox(json_frame, height=5)
        self.json_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.json_listbox.bind("<<ListboxSelect>>", self.on_json_select)
        scrollbar = tk.Scrollbar(json_frame, orient="vertical", command=self.json_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.json_listbox.config(yscrollcommand=scrollbar.set)
        refresh_button = tk.Button(json_frame, text="Refresh", command=self.search_json_files)
        refresh_button.pack(side=tk.BOTTOM, pady=5)
        
        self.search_json_files()
    
    def get_file_name(self):
        name = self.file_entry.get().strip()
        if not name.endswith(".json"):
            name += ".json"
        return name
    
    def update_status(self, msg):
        self.status_label.config(text=f"Status: {msg}")
    
    def append_log(self, msg):
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
    
    def clear_log(self):
        self.log_text.delete("1.0", tk.END)
    
    def browse_file(self):
        file_path = filedialog.askopenfilename(initialdir=os.path.join(os.path.dirname(__file__), "user_training"),
                                               filetypes=[("JSON Files", "*.json")])
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, os.path.basename(file_path))
    
    def search_json_files(self):
        training_dir = os.path.join(os.path.dirname(__file__), "user_training")
        if not os.path.exists(training_dir):
            os.makedirs(training_dir)
        json_files = [f for f in os.listdir(training_dir) if f.lower().endswith('.json')]
        self.json_listbox.delete(0, tk.END)
        for file in json_files:
            self.json_listbox.insert(tk.END, file)
    
    def on_json_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            file_name = event.widget.get(index)
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_name)
