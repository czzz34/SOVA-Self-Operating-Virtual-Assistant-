# functions/personalized_prompt.py
from functions.systeminfo_form import get_latest_system_info

def build_personalized_prompt(user_query: str, conversation_history: str) -> str:
    """
    Build a prompt that includes the latest system info from systeminfo.csv,
    the conversation history, and the current user query.
    """
    user_system_info = get_latest_system_info()
    prompt = (
        "You are a sophisticated AI assistant that personalizes responses based on the user's system information. "
        "Below is the user's system information:\n\n"
        f"{user_system_info}\n\n"
        "Conversation History:\n"
        f"{conversation_history}\n\n"
        "User Query:\n"
        f"{user_query}\n\n"
        "Please respond accordingly."
    )
    return prompt
