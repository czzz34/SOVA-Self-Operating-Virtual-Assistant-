# functions/pdf_summarizer.py

import fitz   # PyMuPDF
import re
import ollama

def summarize_pdf(file_path: str, model: str = "gemma2:9b") -> str:
    """
    Reads a PDF file, extracts its text, and uses the Ollama Gemma2:9b model
    to generate a concise summary.
    """
    # 1) Read and clean the PDF text
    try:
        doc = fitz.open(file_path)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        full_text = re.sub(r'\s+', ' ', full_text).strip()
    except Exception as e:
        return f"❌ Failed to read PDF: {e}"

    # 2) Send to Ollama for summarization
    try:
        # Build a chat prompt
        messages = [
            {"role": "system", "content": "You are a helpful assistant that summarizes documents."},
            {"role": "user",   "content": f"Please provide a concise summary of the following text:\n\n{full_text}"}
        ]
        resp = ollama.chat(model=model, messages=messages)  # :contentReference[oaicite:0]{index=0}
        summary = resp["message"]["content"].strip()
        return summary
    except Exception as e:
        return f"❌ Ollama summarization failed: {e}"
