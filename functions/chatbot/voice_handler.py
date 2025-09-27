# functions/chatbot/voice_handler.py

import threading
import logging
import speech_recognition as sr

from functions.speech import listen_in_background as _listen_bg

class VoiceHandler:
    def start_listening(self) -> None:
        """
        Listen in the background, then send recognized text
        into the GUI as if it were typed.
        """
        threading.Thread(
            target=lambda: _listen_bg(
                self.append_message,
                self.send_voice_text
            ),
            daemon=True
        ).start()

    def send_voice_text(self, text: str) -> None:
        """
        Insert recognized text into the input widget and invoke
        send_message(), so it flows through CommandHandler.
        """
        # Must run on the main Tk thread:
        self.root.after(0, lambda: (
            self.user_input.delete(0, 'end'),
            self.user_input.insert(0, text),
            self.send_message()
        ))

    def speak_last_response(self) -> None:
        for message in reversed(self.chat_history):
            if message.get("role") == "assistant":
                self.speak_text(message.get("content"))
                break

    def speak_text(self, text: str) -> None:
        from functions.speech import speak_text as _speak
        if hasattr(self, 'tts_engine') and self.tts_engine:
            try:
                _speak(self.tts_engine, text)
            except Exception as e:
                logging.error("Error in TTS: %s", e)
        else:
            logging.error("TTS engine is not initialized.")
