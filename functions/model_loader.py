# functions/model_loader.py
import ollama
import logging

def chat_with_model(model: str, messages: list) -> dict:
    """
    Wrapper for ollama.chat to interact with the model.
    """
    try:
        response = ollama.chat(model=model, messages=messages)
        return response
    except Exception as e:
        logging.error("Error during model chat: %s", e)
        raise e

def generate_image_description(model: str, prompt: str, images: list) -> dict:
    """
    Wrapper for ollama.generate to generate image descriptions.
    """
    try:
        response = ollama.generate(model=model, prompt=prompt, images=images)
        return response
    except Exception as e:
        logging.error("Error during image generation: %s", e)
        raise e
