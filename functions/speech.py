# functions/speech.py
import threading
import speech_recognition as sr
import logging

def listen_in_background(append_message_callback, process_ai_response_callback):
    """
    Listens for voice input in the background.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        append_message_callback("System", "Listening... Speak now, genius.", "system_msg")
        try:
            audio = r.listen(source, phrase_time_limit=5)
            recognized_text = r.recognize_google(audio)
            append_message_callback("You (Voice)", recognized_text, "user_msg")
            threading.Thread(target=process_ai_response_callback, args=(recognized_text,), daemon=True).start()
        except Exception as e:
            append_message_callback("System", f"Could not understand audio: {str(e)}", "system_msg")

def speak_text(tts_engine, text):
    """
    Convert given text to speech.
    """
    if tts_engine:
        try:
            tts_engine.say(text)
            tts_engine.runAndWait()
        except Exception as e:
            logging.error("Error in TTS: %s", e)
    else:
        logging.error("TTS engine is not initialized.")
