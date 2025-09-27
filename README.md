SOVA - Self Operating Voice Assistant

SOVA is an offline AI voice assistant that runs locally using Ollama. You can use any LLM model you prefer, though Gemma2:9b is recommended for generating high-quality text outputs.

Features

Offline Local AI: Runs entirely on your machine using Ollama.

Flexible Models: Use any Ollama-supported model (Gemma2:9b recommended).

Voice Interaction: Talk to SOVA and get responses in real-time.

PDF Summarization: Summarize PDFs quickly using voice commands.

Music Playback: Play music using yt_dlp (requires internet).

Web Commands: Access and control SOVA from other devices on the same LAN using the GUI IP.

Modular and Extensible: Easily add new features or integrate other functionalities.

Installation

Clone the repository:

git clone https://github.com/yourusername/SOVA.git
cd SOVA


Install required Python packages:

pip install -r requirements.txt


Ensure you have Ollama installed and the desired model pulled:

ollama pull gemma2:9b

Usage

Run the assistant:

python main.py


GUI Instructions:

The assistant GUI will show an IP address on top.

You can connect from another device on the same LAN to issue commands.

Voice Commands:

Ask SOVA to summarize PDFs, play music, or perform other tasks.

Some functions (like music playback) require internet connectivity.

File Structure
SOVA/
│
├─ main.py             # Entry point
├─ modules/            # Individual features (music, PDF, etc.)
├─ functions/          # Helper scripts (e.g., weather.py)
├─ resources/          # Audio, images, config files
├─ ui/                 # GUI components
├─ .env                # Environment variables (optional)
└─ README.md

Notes

Make sure your .env file (if any) is configured properly.

Music playback requires an active internet connection, while most other functionalities work offline.

You can change the AI model in Ollama to any supported model; Gemma2:9b is just a recommendation.
