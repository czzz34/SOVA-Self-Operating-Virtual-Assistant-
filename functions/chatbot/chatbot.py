# functions/chatbot/chatbot.py

import tkinter as tk
import threading
import time
import logging

try:
    import pyttsx3
except Exception as e:
    logging.error("TTS engine initialization failed: %s", e)
    pyttsx3 = None

from functions.chatbot.ui_manager import UIManager
from functions.chatbot.command_handler import CommandHandler
from functions.chatbot.ai_interaction import AIInteraction
from functions.chatbot.followup import FollowUp
from functions.chatbot.voice_handler import VoiceHandler
from functions.chatbot.hardware_handler import HardwareHandler
from functions.chatbot.personality_handler import PersonalityHandler

# Import our new screenshot capturer (if available)
try:
    from functions.screenshot_capturer import take_screenshots
except ImportError as ie:
    logging.error("Screenshot capturer import failed: %s", ie)
    take_screenshots = None

# Import the play_music function that handles YouTube search + audio playback
from functions.chatbot.music_player import play_music


class ChatBot(
    UIManager,
    CommandHandler,
    AIInteraction,
    FollowUp,
    VoiceHandler,
    HardwareHandler
):
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("TARS - AI Chatbot")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{int(screen_width * 0.3)}x{int(screen_height * 0.7)}")
        self.root.configure(bg="#2C2F33")

        # Initialize TTS engine (if available)
        if pyttsx3 is not None:
            try:
                self.tts_engine = pyttsx3.init()
            except Exception as e:
                logging.error("TTS engine init failed: %s", e)
                self.tts_engine = None
        else:
            self.tts_engine = None

        # Chat prompts & history
        self.visible_prompt = "Default personality prompt: I am TARS, your AI assistant."
        self.abstract_prompt = "Abstract instructions for TARS."
        self.chat_history = [{"role": "system", "content": self.visible_prompt}]
        self.last_input_time = time.time()

        # Shared stop event for background threads
        self.stop_event = threading.Event()

        # Build the GUI
        self.setup_ui()

        # “Voice Command” / personality button
        self.personality_handler = PersonalityHandler(self)
        self.personality_button = tk.Button(
            self.root,
            text="Voice Command",
            command=self.start_listening,
            bg="#7289DA",
            fg="white",
            font=("Arial", 12, "bold")
        )
        self.personality_button.grid(
            row=10, column=0, columnspan=3, padx=10, pady=5, sticky="ew"
        )

        # Start follow-up thread (for periodic reminders or health checks)
        threading.Thread(target=self.start_followup_async, daemon=True).start()

        # Start screenshot thread (if available)
        if take_screenshots:
            threading.Thread(
                target=take_screenshots,
                args=(1.0, self.stop_event),  # interval = 1s
                daemon=True
            ).start()

    def open_personality_window(self):
        self.personality_handler.open_personality_window()

    def open_self_training(self):
        from functions.chatbot.self_training import SelfTrainingWindow
        SelfTrainingWindow(self.root)

    def on_closing(self) -> None:
        # Signal all background threads (follow-up, screenshots) to stop
        self.stop_event.set()
        # Then destroy the Tkinter window
        self.root.destroy()

    def handle_play_command(self, query: str):
        """
        Search YouTube for `query`, extract the best audio stream, and play it.
        This runs in a background thread so the GUI remains responsive.

        Usage from GUI:
            threading.Thread(
                target=self.handle_play_command,
                args=(search_query,),
                daemon=True
            ).start()
        """
        # Notify user in chat window
        self.append_message("You", f"Requested to play: {query}", "user_msg")
        self.append_message("TARS", f"Playing audio for: {query}", "ai_msg")

        # Launch playback in a separate thread
        def _play():
            try:
                play_music(query)
            except Exception as e:
                # On error, report back in the chat window
                self.root.after(
                    0,
                    lambda: self.append_message("TARS", f"Could not play '{query}': {e}", "ai_msg")
                )

        threading.Thread(target=_play, daemon=True).start()

    # You can override or extend other chatbot methods here as needed.
    # For example, if you want “play <term>” to be detected automatically,
    # you could override CommandHandler.send_message() or add a check
    # in UIManager’s input-binding logic. But as a minimal example, handle_play_command
    # should be called explicitly when your GUI detects “play …”.

