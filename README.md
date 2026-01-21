

---

# ![SOVA Logo](https://img.icons8.com/fluency/48/000000/robot-2.png) SOVA - Self Operating Voice Assistant

**SOVA** is an **offline AI voice assistant** that runs locally using Ollama. You can use any LLM model you prefer, though **Gemma2:9b** is recommended for generating high-quality text outputs.

---

## 🌟 Features

* **Offline Local AI:** Runs entirely on your machine using Ollama.
* **Flexible Models:** Use any Ollama-supported model (`Gemma2:9b` recommended).
* **Voice Interaction:** Talk to SOVA and receive real-time responses.
* **PDF Summarization:** Summarize PDFs quickly via voice commands.
* **Music Playback:** Play music using `yt_dlp` (**requires internet**).
* **Web Commands:** Control SOVA from other devices on the same LAN using the GUI IP.
* **Modular & Extensible:** Easily add new features or integrate other functionalities.

---

## 🛠️ Installation

1. **Clone the repository:**

```bash
git clone https://github.com/czzz34/SOVA-Self-Operating-Virtual-Assistant-.git
cd SOVA
```

2. **Install required Python packages:**

```bash
pip install -r requirements.txt
```

3. **Ensure Ollama is installed and the desired model is pulled:**

```bash
ollama pull gemma2:9b
```

---

## 🚀 Usage

1. **Run the assistant:**

```bash
python main.py
```

2. **GUI Instructions:**

   * The assistant GUI displays an **IP address** on top.
   * Connect from another device on the same LAN to issue commands.

3. **Voice Commands:**

   * Summarize PDFs, play music, or perform other tasks.
   * Music playback requires an **active internet connection**; other functions work offline.

---

## 📂 File Structure

```
SOVA/
│
├─ main.py             # Entry point
├─ functions/          # Helper scripts 
├─ .env                # Environment variables
└─ README.md
```

---

## ⚠️ Notes


* You can switch the AI model in Ollama; `Gemma2:9b` is only a recommendation.
* Functions like music playback require an internet connection.
