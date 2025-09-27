# functions/chatbot/command_handler.py

import threading
import time
import logging
import pyautogui
import os
import webbrowser
from tkinter import simpledialog
import asyncio
from difflib import get_close_matches

from functions.utility import type_like_human, open_windows_search, interpret_open_command
from functions.hardware import generate_response
from functions.model_loader import chat_with_model, generate_image_description

# Macro‑selection for self‑training
from functions.chatbot.self_training import get_json_filenames
from functions.chatbot.macro_selector import select_macro_file

# Special “project‑or‑creator” queries
from functions.chatbot.special_queries import handle_special_query


class CommandHandler:
    def send_message(self, event=None) -> None:
        # 1) special canned answers
        user_text = self.user_input.get().strip()
        special = handle_special_query(user_text)
        if special:
            self.append_message("TARS", special, "ai_msg")
            self.user_input.delete(0, "end")
            return

        # 2) ignore blank
        if not user_text:
            return

        lower_text = user_text.lower()

        # 3) play <query>
        if lower_text.startswith("play "):
            query = user_text[5:].strip()
            if query:
                self.handle_play_command(query)
            self.user_input.delete(0, "end")
            return

        # 4) volume set <n>
        if lower_text.startswith("volume set "):
            vol_part = user_text[11:].strip()
            try:
                vol_val = int(vol_part)
                vol_val = max(0, min(vol_val, 100))
                self.handle_volume_set(vol_val)
            except ValueError:
                self.append_message("TARS", f"Invalid volume: {vol_part}", "ai_msg")
            self.user_input.delete(0, "end")
            return

        # 5) normal flow: show user message + AI/macro
        self.append_message("You", user_text, "user_msg")
        self.user_input.delete(0, "end")
        self.last_input_time = time.time()
        self.waiting_for_reply = True

        # 5a) “open …” goes to macro subsystem
        if lower_text.startswith("open ") or lower_text.startswith("can you open "):
            threading.Thread(
                target=self.run_macro_for_command,
                args=(user_text,),
                daemon=True
            ).start()
        # 5b) everything else → AI
        else:
            threading.Thread(
                target=self.process_ai_response,
                args=(user_text,),
                daemon=True
            ).start()

    def process_ai_response(self, user_message: str) -> None:
        """
        Hand off to the AIInteraction layer or health/mood generator.
        """
        if self.is_health_query(user_message):
            mood_response = generate_response()
            self.root.after(0, lambda: self.append_message("TARS", mood_response, "ai_msg"))
        else:
            ai_reply = self.chat_with_ai(user_message)
            self.root.after(0, lambda: self.append_message("TARS", ai_reply, "ai_msg"))

        self.waiting_for_reply = False

    def launch_app(self, command: str = None) -> None:
        """
        Opens an app, folder, or website based on interpret_open_command().
        """
        if command is None:
            command = simpledialog.askstring("Open Command", "Enter what to open:")
            if not command:
                return
        else:
            low = command.lower()
            if low.startswith("open "):
                command = command[5:]
            elif low.startswith("can you open "):
                command = command[13:]

        cmd = interpret_open_command(command)
        if cmd.get("type") == "app" and ":" in cmd.get("target", "") and "\\" in cmd.get("target", ""):
            # If it's an exe path, treat as folder so Windows will open it
            cmd["type"] = "folder"

        self.append_message("You", f"Request: {command} interpreted as {cmd}", "user_msg")

        def _run():
            if cmd["type"] == "app":
                if cmd.get("secondary"):
                    pyautogui.press('winleft')
                    type_like_human(cmd["target"])
                    pyautogui.press('enter')
                    type_like_human(cmd["secondary"])
                    pyautogui.press('enter')
                    result = f"✅ Opened {cmd['target']} and searched '{cmd['secondary']}'"
                else:
                    result = open_windows_search(cmd["target"])
            elif cmd["type"] == "website":
                webbrowser.open(cmd["target"])
                result = f"✅ Opened webpage '{cmd['target']}'"
            elif cmd["type"] == "folder":
                try:
                    os.startfile(cmd["target"])
                    result = f"✅ Opened folder '{cmd['target']}'"
                except Exception as e:
                    result = f"Error opening folder: {e}"
            else:
                result = f"Command type {cmd.get('type')} not recognized."

            self.root.after(0, lambda: self.append_message("TARS", result, "ai_msg"))

        threading.Thread(target=_run, daemon=True).start()

    # --- Macro replay (sync & async) ---
    def run_macro_for_command(self, command: str) -> None:
        json_files = get_json_filenames()
        chosen = select_macro_file(command, json_files)
        if chosen and chosen.lower() != "none":
            self.append_message("TARS", f"Selected macro: {chosen}", "ai_msg")
            threading.Thread(target=lambda: self._replay_macro(chosen), daemon=True).start()
        else:
            self.append_message("TARS", "No suitable macro found.", "ai_msg")

    def _replay_macro(self, file_name: str) -> None:
        from functions.chatbot.self_training import MacroRecorderPlayer
        macro = MacroRecorderPlayer(lambda *_: None, lambda *_: None)
        macro.replay_events(file_name)

    async def async_run_macro_for_command(self, command: str) -> None:
        loop = asyncio.get_event_loop()
        json_files = get_json_filenames()
        chosen = await loop.run_in_executor(None, select_macro_file, command, json_files)
        if chosen and chosen.lower() != "none":
            self.root.after(
                0,
                lambda: self.append_message("TARS", f"Selected macro: {chosen}", "ai_msg")
            )
            await loop.run_in_executor(None, self._replay_macro, chosen)
        else:
            self.root.after(0, lambda: self.append_message("TARS", "No suitable macro found.", "ai_msg"))
