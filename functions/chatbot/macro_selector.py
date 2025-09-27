import json
import logging
import re
import threading
import time
import asyncio
from difflib import get_close_matches
from functions.model_loader import chat_with_model
from functions.chatbot.self_training import get_json_filenames, MacroRecorderPlayer

def select_macro_file(command: str, json_files: list) -> str:
    """
    Sends a prompt to the model with the available JSON macro files and the user command.
    The model should return descriptive text including a recommended file name.
    This function first uses a case-insensitive regex to extract any word ending with '.json'.
    If an exact candidate (normalized for case) is found in the available list, it is returned.
    Otherwise, it falls back to a nearest-neighbor approach.
    """
    prompt = (
        "You are a macro selection assistant. "
        "I have the following JSON files that record macros for controlling applications:\n"
        f"{json.dumps(json_files)}\n\n"
        "For example, 'youtubeopener.json' is used to simply open YouTube, "
        "while 'youtubeopeneandplay1stvideor.json' performs extra actions like playing a video. "
        "Based on the user command below, please return the file name that best matches the intended action. "
        "Your response may include extra descriptive text, but it must contain a file name ending with '.json'.\n\n"
        f"User command: {command}"
    )
    
    try:
        response = chat_with_model("gemma2:9b", messages=[{"role": "system", "content": prompt}])
        response_text = response["message"]["content"].strip()
        logging.info("Macro selector raw response: %s", response_text)
        
        # Extract candidate file names (case-insensitive) ending with .json
        candidates = re.findall(r"\b[\w\-]+\.json\b", response_text, re.IGNORECASE)
        if candidates:
            # Normalize candidate and available file names for case-insensitive comparison
            candidates_lower = [c.lower() for c in candidates]
            json_files_lower = [f.lower() for f in json_files]
            for candidate in candidates_lower:
                if candidate in json_files_lower:
                    chosen_file = json_files[json_files_lower.index(candidate)]
                    logging.info("Exact candidate extracted: %s", chosen_file)
                    return chosen_file
            logging.warning("Extracted candidates %s not found in available list.", candidates)
        
        # Fallback: use difflib's nearest neighbor matching on the entire response text
        best_matches = get_close_matches(response_text.lower(), json_files_lower, n=1, cutoff=0.3)
        if best_matches:
            chosen_file = json_files[json_files_lower.index(best_matches[0])]
            logging.info("Chosen file via nearest neighbor fallback: %s", chosen_file)
            return chosen_file
        else:
            logging.error("No close match found for response: '%s'", response_text)
            return None
    except Exception as e:
        logging.error("Error in macro selection: %s", e)
        return None

class MacroCommandHandler:
    """
    A command handler for executing macros.
    When given a command (e.g. "open youtube and search valorant"), it selects the best JSON macro file
    and then replays the macro (e.g. using pyautogui to type "valorant" and press Enter).
    """
    def __init__(self, root, append_message_callback):
        """
        Parameters:
            root: The Tkinter root window (for scheduling UI updates)
            append_message_callback: A function to update the UI with messages (e.g. append_message(sender, message, tag))
        """
        self.root = root
        self.append_message = append_message_callback
        self.last_input_time = time.time()
    
    def run_macro_for_command(self, command: str) -> None:
        """
        Synchronously selects a macro file based on the command and replays it.
        """
        json_files = get_json_filenames()
        chosen_file = select_macro_file(command, json_files)
        if chosen_file and chosen_file.lower() != "none":
            self.root.after(0, lambda: self.append_message("TARS", f"Selected macro: {chosen_file}", "ai_msg"))
            threading.Thread(target=lambda: self._replay_macro(chosen_file), daemon=True).start()
        else:
            self.root.after(0, lambda: self.append_message("TARS", "No suitable macro found.", "ai_msg"))
    
    def _replay_macro(self, file_name: str) -> None:
        """
        Replays the macro recorded in the given JSON file.
        """
        macro_player = MacroRecorderPlayer(lambda msg: None, lambda msg: None)
        macro_player.replay_events(file_name)
    
    async def async_run_macro_for_command(self, command: str) -> None:
        """
        Asynchronously selects a macro file and replays it.
        """
        loop = asyncio.get_event_loop()
        json_files = get_json_filenames()
        chosen_file = await loop.run_in_executor(None, select_macro_file, command, json_files)
        if chosen_file and chosen_file.lower() != "none":
            self.root.after(0, lambda: self.append_message("TARS", f"Selected macro: {chosen_file}", "ai_msg"))
            await loop.run_in_executor(None, self._replay_macro, chosen_file)
        else:
            self.root.after(0, lambda: self.append_message("TARS", "No suitable macro found.", "ai_msg"))
