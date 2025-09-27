# functions/utility.py
import json
import logging
import pyautogui
import webbrowser
import os
from functions.prompt_builder import get_interpretation_prompt
from functions.model_loader import chat_with_model

def type_like_human(text: str) -> None:
    """
    Simulate human-like typing by writing each character with a random delay.
    """
    for char in text:
        pyautogui.write(char)

def open_windows_search(app_name: str) -> str:
    """
    Opens an application via Windows search.
    """
    pyautogui.press('winleft')
    type_like_human(app_name)
    pyautogui.press('enter')
    message = f"✅ Opened {app_name}"
    logging.info(message)
    return message

def interpret_open_command(command: str) -> dict:
    """
    Use the prompt to interpret an 'open' command.
    Returns a dict with keys: 'type', 'target', and optionally 'secondary'.
    """
    prompt = get_interpretation_prompt()
    try:
        response = chat_with_model("gemma2:9b", messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": command}
        ])
        content = response["message"]["content"].strip()
        if not content:
            raise ValueError("Empty response")
        result = json.loads(content)
        logging.info(f"Interpreted command: {result}")
        return result
    except Exception as e:
        logging.error("Error interpreting command with Ollama: %s", e)
        return {"type": "app", "target": command}
