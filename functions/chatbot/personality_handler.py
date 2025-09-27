import os
import tkinter as tk
from tkinter import ttk, messagebox

class PersonalityHandler:
    def __init__(self, chatbot_instance):
        """Initialize with a reference to the main ChatBot instance."""
        self.chatbot = chatbot_instance  # Store reference to ChatBot
        self.root = chatbot_instance.root  # Access main Tkinter window
        self.chat_history = chatbot_instance.chat_history  # Access chat history

    def open_personality_window(self):
        """Opens a window to let the user choose a personality."""
        self.personality_window = tk.Toplevel(self.root)
        self.personality_window.title("Select Personality")
        self.personality_window.geometry("400x400")

        label = tk.Label(self.personality_window, text="Select a Personality:", font=("Arial", 14))
        label.pack(pady=10)

        # Create a listbox to display personality options
        self.personality_listbox = tk.Listbox(self.personality_window, font=("Arial", 12))
        self.personality_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Load personality options from the "personality" directory
        personality_dir = os.path.join(os.getcwd(), "personality")
        if not os.path.exists(personality_dir):
            os.makedirs(personality_dir)  # Create if not exists

        self.personality_files = [f for f in os.listdir(personality_dir) if f.lower().endswith(".txt")]
        
        if not self.personality_files:
            self.personality_listbox.insert(tk.END, "No personality files found.")
        else:
            self.personality_files.sort()
            for file in self.personality_files:
                display_name = os.path.splitext(file)[0]  # Remove .txt extension for display
                self.personality_listbox.insert(tk.END, display_name)

        apply_btn = ttk.Button(self.personality_window, text="Apply", command=self.apply_personality)
        apply_btn.pack(pady=10)

    def apply_personality(self):
        """Loads the selected personality and updates chatbot behavior."""
        selection = self.personality_listbox.curselection()

        if not selection:
            messagebox.showerror("Error", "Please select a personality.")
            return

        index = selection[0]

        # Prevent index error
        if index >= len(self.personality_files):
            messagebox.showerror("Error", "Invalid selection.")
            return

        selected_personality = self.personality_files[index]
        personality_dir = os.path.join(os.getcwd(), "personality")
        file_path = os.path.join(personality_dir, selected_personality)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                personality_prompt = f.read().strip()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load personality: {e}")
            return

        # Update ChatBot's personality prompt
        self.chatbot.visible_prompt = personality_prompt  

        # Reset the system message in chat history
        if self.chat_history:
            self.chat_history[0] = {"role": "system", "content": personality_prompt}
        else:
            self.chat_history.append({"role": "system", "content": personality_prompt})

        messagebox.showinfo("Success", "Personality has been updated!")
        self.personality_window.destroy()
