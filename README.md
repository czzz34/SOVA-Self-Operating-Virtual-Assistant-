# ![SOVA Logo](https://img.icons8.com/fluency/48/000000/robot-2.png) SOVA - Self Operating Voice Assistant

A powerful **offline AI voice assistant** that runs entirely on your local machine using [Ollama](https://ollama.ai/). SOVA combines the power of large language models with intuitive voice interaction, bringing AI capabilities to your desktop without relying on cloud services or internet connectivity.

---

## 🌟 Key Features

- **🚀 Offline & Local:** Runs entirely on your machine using Ollama—no cloud dependencies, complete privacy
- **🎤 Voice Interaction:** Communicate naturally with your AI assistant through voice commands
- **📚 PDF Summarization:** Quickly summarize PDF documents via voice commands
- **🎵 Music Playback:** Stream and play music (requires internet connection)
- **🌐 LAN Web Interface:** Control SOVA from other devices on your local network using a graphical interface
- **🔧 Flexible Model Support:** Use any Ollama-supported LLM model (Gemma2:9b recommended)
- **📦 Modular Architecture:** Easily extend functionality with custom modules and integrations
- **⚡ Fast & Responsive:** Real-time voice processing with minimal latency

---

## 📋 Requirements

Before installation, ensure you have the following:

- **Python 3.8+** - Download from [python.org](https://www.python.org/)
- **Ollama** - Download from [ollama.ai](https://ollama.ai/)
- **Gemma2:9b** or another LLM model (pulled via Ollama)
- **Microphone** - For voice input
- **Audio Output** - For voice responses and music playback

### System Requirements

- **RAM:** 8GB minimum (16GB recommended for smooth operation)
- **Disk Space:** 10GB+ for model storage
- **Processor:** Multi-core CPU recommended
- **OS:** Linux, macOS, or Windows

---

## 🛠️ Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/czzz34/SOVA-Self-Operating-Virtual-Assistant-.git
cd SOVA
```

### Step 2: Set Up Python Environment (Optional but Recommended)

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install and Configure Ollama

1. **Download and install Ollama** from [ollama.ai](https://ollama.ai/)
2. **Pull the recommended model:**

```bash
ollama pull gemma2:9b
```

> **Note:** You can use any Ollama-supported model. Other popular options include:
> - `llama2` - Fast and lightweight
> - `mistral` - Good for coding tasks
> - `neural-chat` - Optimized for conversations

### Step 5: Configure Environment Variables

Create a `.env` file in the project root:

```env
# Ollama Configuration
OLLAMA_MODEL=gemma2:9b
OLLAMA_HOST=http://localhost:11434

# Voice Settings (optional)
VOICE_LANGUAGE=en-US
```

---

## 🚀 Quick Start

### Basic Usage

1. **Start the SOVA Assistant:**

```bash
python main.py
```

2. **Access the GUI:**
   - The assistant will display an **IP address** in the console output (e.g., `http://192.168.1.100:5000`)
   - Open this address in your web browser on any device on your local network
   - Use the GUI to send voice commands or text input

3. **Try Voice Commands:**
   - "Summarize the PDF on my desktop"
   - "Play some music"
   - "What is the weather like?" (offline response based on your model)

### Running from Another Device

1. Both devices must be on the **same LAN**
2. Open the displayed IP address in your browser from the other device
3. Send commands through the web interface

---

## 📁 Project Structure

```
SOVA/
│
├── main.py                    # Main entry point - starts the assistant
├── requirements.txt           # Python dependencies
├── .env                       # Environment configuration (create this)
├── .gitignore                 # Git ignore patterns
├── README.md                  # This file
│
├── functions/                 # Helper modules and feature scripts
│   ├── __init__.py
│   ├── voice_handler.py      # Voice input/output processing
│   ├── pdf_summarizer.py     # PDF summarization logic
│   ├── music_player.py       # Music playback functionality
│   └── ollama_handler.py     # Ollama LLM integration
│
├── static/                   # Web GUI assets (if applicable)
│   ├── css/
│   ├── js/
│   └── index.html
│
└── logs/                     # Application logs (auto-generated)
    └── sova.log
```

---

## 🎯 Usage Examples

### Voice Command Examples

| Command | Function | Requires Internet |
|---------|----------|------------------|
| "Summarize this PDF" | Analyzes and summarizes a PDF file | No |
| "Play music" | Starts music playback | Yes |
| "Tell me a joke" | Generates humorous responses | No |
| "Write a poem" | Creative text generation | No |
| "Help me debug this code" | Code analysis and suggestions | No |

### API Integration

To integrate SOVA into your own application:

```python
from functions.ollama_handler import OllamaHandler
from functions.voice_handler import VoiceProcessor

# Initialize components
llm = OllamaHandler(model="gemma2:9b")
voice = VoiceProcessor()

# Process user input
user_input = voice.record()
response = llm.generate(user_input)
voice.speak(response)
```

---

## ⚙️ Configuration

### Switching AI Models

Edit `.env` or modify directly in code:

```env
OLLAMA_MODEL=mistral  # or any other Ollama model
```

Supported models: `llama2`, `mistral`, `neural-chat`, `codellama`, etc.

### Audio Settings

Configure voice recognition and synthesis in `main.py`:

```python
VOICE_LANGUAGE = "en-US"        # Language code
SPEECH_RATE = 1.0               # Speaking speed (0.5 - 2.0)
MICROPHONE_INDEX = 0            # Microphone device index
```

### Port Configuration

By default, SOVA runs on port 5000. To change:

```bash
# Set the Flask port before running
export FLASK_PORT=8080
python main.py
```

---

## 🌐 Network Usage

### Local Network Access

- **Default Port:** 5000
- **Access URL:** `http://<your-machine-ip>:5000`
- Find your machine's IP:
  - **Linux/macOS:** `ifconfig | grep "inet "`
  - **Windows:** `ipconfig`

### Firewall Configuration

Allow port 5000 through your firewall:

```bash
# Linux (Ubuntu/Debian)
sudo ufw allow 5000

# macOS (if using firewall)
sudo /usr/libexec/ApplicationFirewall/socketfilterfw -k
```

---

## 📊 Features in Detail

### 🎤 Voice Processing

- Real-time speech recognition
- Natural language understanding via Ollama
- Text-to-speech output
- Multiple language support

### 📄 PDF Summarization

- Extracts text from PDFs
- Generates concise summaries using the LLM
- Preserves key information
- Works completely offline

### 🎵 Music Playback

- Integration with `yt_dlp` for music streaming
- Queue management
- Playback controls via GUI
- **Requires internet connection**

### 🔐 Privacy & Security

- All processing happens locally
- No data sent to external servers
- Models stored locally on your machine
- Complete control over your data

---

## 🐛 Troubleshooting

### Issue: "Ollama connection refused"

**Solution:** Ensure Ollama is running

```bash
# Start Ollama service
ollama serve

# In another terminal, verify connection
curl http://localhost:11434/api/tags
```

### Issue: "Microphone not detected"

**Solution:** Check audio device

```python
import speech_recognition as sr
recognizer = sr.Recognizer()
mic = sr.Microphone()
print(sr.Microphone.list_microphone_indexes())
```

### Issue: "Model not found"

**Solution:** Pull the model

```bash
ollama pull gemma2:9b
```

### Issue: Poor voice recognition

- Reduce background noise
- Speak clearly and at normal pace
- Check microphone levels
- Try a different model

### Issue: Slow responses

- Close other applications
- Reduce background processes
- Consider using a lighter model
- Check your system RAM

---

## 📦 Dependencies

Core dependencies (see `requirements.txt`):

- **ollama** - LLM integration
- **Flask** - Web server for GUI
- **SpeechRecognition** - Voice input processing
- **pyttsx3** - Text-to-speech
- **PyPDF2** - PDF processing
- **yt_dlp** - Music streaming
- **python-dotenv** - Environment variable management

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Development Setup

```bash
pip install -r requirements.txt
pip install pytest black flake8  # Development tools

# Run tests
pytest

# Format code
black .

# Lint code
flake8 .
```

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) - For the amazing local LLM platform
- [OpenAI Speech Recognition](https://github.com/openai/whisper) - Inspiration for voice processing
- Contributors and testers

---

## 📧 Support & Contact

- **GitHub Issues:** [Report bugs](https://github.com/czzz34/SOVA-Self-Operating-Virtual-Assistant-/issues)
- **Discussions:** [Join discussions](https://github.com/czzz34/SOVA-Self-Operating-Virtual-Assistant-/discussions)
- **Author:** [@czzz34](https://github.com/czzz34)

---

## 🗺️ Roadmap

- [ ] Multi-language support expansion
- [ ] Integration with smart home devices
- [ ] Advanced context memory
- [ ] Custom voice profiles
- [ ] Web UI improvements
- [ ] Docker containerization
- [ ] Mobile app companion

---

## ⭐ If you find this project useful, please consider giving it a star!

---

**Last Updated:** January 2026 | **Status:** Active Development
