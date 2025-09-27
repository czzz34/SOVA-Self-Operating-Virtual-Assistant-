import socket
import tkinter as tk
from tkinter import filedialog, ttk
from datetime import datetime
import threading
from functions.conversation_logger import log_message
from functions.pdf_summarizer import summarize_pdf

class UIManager:
    def setup_ui(self):
        # --- 1) Determine local IP address ---
        ip = self._get_local_ip()
        
        # --- 2) IP banner at the top ---
        self.ip_label = ttk.Label(
            self.root,
            text=f"IP Address: {ip}",
            font=("Arial", 10, "bold"),
            background="#1F2833",
            foreground="white",
            anchor="center"
        )
        self.ip_label.grid(row=0, column=0, columnspan=3, sticky="ew", padx=10, pady=(10, 0))

        # --- 3) Chat display (shifted down to row=1) ---
        self.chat_display = tk.Text(
            self.root, wrap=tk.WORD, state='disabled', width=60, height=20,
            bg="#23272A", fg="white", font=("Arial", 12), padx=10, pady=10
        )
        self.chat_display.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.chat_display.bind("<Button-3>", self.show_context_menu)

        # --- 4) User input row (row=2) ---
        self.user_input = ttk.Entry(self.root, font=("Arial", 12))
        self.user_input.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        self.user_input.bind("<Return>", self.send_message)

        self.send_button = ttk.Button(
            self.root, text="Send", command=self.send_message, style="Accent.TButton"
        )
        self.send_button.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.pdf_button = ttk.Button(
            self.root, text="Summarize PDF", command=self.load_and_summarize_pdf
        )
        self.pdf_button.grid(row=2, column=2, padx=10, pady=5, sticky="ew")

        # --- 5) Status label (row=3) ---
        self.status_var = tk.StringVar(value="Status: Idle")
        self.status_label = ttk.Label(
            self.root, textvariable=self.status_var, font=("Arial", 10, "italic"),
            background="#2C2F33", foreground="white"
        )
        self.status_label.grid(row=3, column=0, columnspan=3, pady=(0,10), sticky="w", padx=10)

        # --- 6) Context menu setup ---
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Clear Chat", command=self.clear_chat)
        self.context_menu.add_command(label="Launch App", command=self.launch_app)
        self.context_menu.add_command(label="Hardware Status", command=self.show_hardware_status)
        self.context_menu.add_command(label="Voice Input", command=self.start_listening)
        self.context_menu.add_command(label="Speak Last Response", command=self.speak_last_response)
        self.context_menu.add_command(label="Self Training", command=self.open_self_training)
        self.context_menu.add_command(label="Change Personality", command=self.open_personality_window)
        self.context_menu.add_command(label="Toggle Theme", command=self.toggle_theme)
        self.context_menu.add_command(label="Summarize PDF", command=self.load_and_summarize_pdf)

        # --- 7) Styles ---
        self.style = ttk.Style()
        self.style.configure("Accent.TButton", foreground="white", background="#7289DA", font=("Arial", 12, "bold"))
        self.style.configure("TButton", padding=6)

        # --- 8) Make chat_display expand ---
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # --- 9) Theme tracking ---
        self.current_theme = "dark"

        # --- 10) Bind NumPad-0 globally to trigger Voice Input ---
        # Using bind_all to catch keypad 0 regardless of widget focus
        self.root.bind_all('<KeyPress-KP_0>', lambda event: self.start_listening())
        # For NumLock=off scenarios, also bind the '0' key on keypad
        self.root.bind_all('<KeyPress-0>', lambda event: self.start_listening())

    def _get_local_ip(self) -> str:
        """
        Returns the local IP address by opening a dummy UDP socket.
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect(("8.8.8.8", 80))
            ip = sock.getsockname()[0] + ":5000"

        except Exception:
            ip = "127.0.0.1"
        finally:
            sock.close()
        return ip

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def append_message(self, sender: str, message: str, tag: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"[{timestamp}] {sender}: {message}\n\n", tag)
        self.chat_display.config(state='disabled')
        self.chat_display.yview(tk.END)
        threading.Thread(target=lambda: log_message(sender, message), daemon=True).start()
        if sender == "TARS" and hasattr(self, 'tts_engine'):
            threading.Thread(target=self.speak_text, args=(message,), daemon=True).start()

    def clear_chat(self) -> None:
        self.chat_display.config(state='normal')
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state='disabled')

    def change_theme(self, theme: str) -> None:
        if theme.lower() == "light":
            self.chat_display.config(bg="white", fg="black")
            self.status_label.config(background="white", foreground="black")
            self.user_input.config(background="white", foreground="black")
            self.style.configure("Accent.TButton", foreground="black", background="#ADD8E6")
            self.root.config(bg="white")
        else:
            self.chat_display.config(bg="#23272A", fg="white")
            self.status_label.config(background="#2C2F33", foreground="white")
            self.user_input.config(background="#40444B", foreground="white")
            self.style.configure("Accent.TButton", foreground="white", background="#7289DA")
            self.root.config(bg="#2C2F33")

    def toggle_theme(self) -> None:
        new_theme = "light" if self.current_theme == "dark" else "dark"
        self.change_theme(new_theme)
        self.current_theme = new_theme

    def load_and_summarize_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not file_path:
            return
        self.status_var.set("Status: Summarizing PDF…")
        def worker():
            summary = summarize_pdf(file_path)
            self.append_message("TARS", f"📄 PDF Summary:\n{summary}", "bot")
            self.status_var.set("Status: Idle")
        threading.Thread(target=worker, daemon=True).start()
    def speak_text(self, text: str) -> None:
        """
        Uses the TTS engine to speak the provided text.
        """
        if hasattr(self, 'tts_engine') and self.tts_engine is not None:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"Error in TTS: {e}")
        else:
            print("TTS engine not initialized or available.")