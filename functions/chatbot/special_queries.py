# functions/chatbot/special_queries.py

# Canned descriptions
_PROJECT_DESC = (
    "This project is 'SOVA - AI Chatbot', a modular Python/Tkinter application that integrates "
    "voice, hardware control, personality switching, PDF summarization, and large-language-model AI. "
    "It uses Ollama's Gemma2:9b for deep reasoning, PyMuPDF for PDF parsing, and can be extended "
    "with new modules via a clean function-based architecture. "
    "This project is a  a   reimagined version of self operating computer  repository which uses paid ai model to interact with system "
    "and  privategpt a gpt in which we can run our own gpt at local server and  chat with pdfs or any other text data also "

)
_CREATOR_DESC = (
    "I was created by Chaitanya , a BCA student and developer passionate about AI automation, "
    "accessibility, and human–computer interaction. Chaitanya designed TARS to showcase modular AI "
    "integration and to serve as a personal productivity assistant."
)

def handle_special_query(text: str) -> str | None:
    """
    If the text asks about the project or its creator, returns the canned response.
    Otherwise returns None.
    """
    lower = text.lower()
    if any(kw in lower for kw in ("project info", "what is self operating virtual assistant", "about this project")):
        return _PROJECT_DESC
    if any(kw in lower for kw in (" your creator", "who made you", "who created you")):
        return _CREATOR_DESC
    return None
