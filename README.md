# gnomi

A lightweight, aesthetic floating AI assistant that integrates with GroqCloud, summoned with Alt+A keyboard shortcut.

## Features

- **Floating Window**: Always-on-top AI assistant window
- **Global Hotkey**: Alt+A to toggle window visibility
- **GroqCloud Integration**: Access to all GroqCloud models (Llama, Mixtral, Gemma)
- **Dark Theme**: Beautiful, minimal dark interface
- **Lightweight**: Minimal resource usage
- **Easy Setup**: Simple installation and configuration

## Quick Start

### Automatic Setup (Recommended)

```bash
# Clone or download this repository
cd ai-assistant

# Run the setup script
./setup.sh

# Start the application
./start_ai_assistant.sh
```

### Manual Setup

1. **Install System Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3 python3-tk python3-pip python3-venv
   ```

2. **Set Up Python Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   source venv/bin/activate
   python run.py
   ```

## 🎮 Usage

1. **Start the Application**: Run `./start_ai_assistant.sh`
2. **Toggle Window**: Press `Alt+A` to show/hide the AI window
3. **First Time Setup**: Enter your GroqCloud API key in the settings
4. **Chat**: Type your question and press Enter
5. **Close**: Press `Alt+A` again or `Escape` to hide the window

## API Key Setup

1. Visit [GroqCloud Console](https://console.groq.com/)
2. Create a free account
3. Generate an API key
4. Click the ⚙️ settings button in the AI assistant
5. Enter your API key

## Available Models

- **llama-3.1-8b-instant** (Fast, efficient)
- **llama-3.1-70b-versatile** (Powerful, balanced)
- **mixtral-8x7b-32768** (Large context window)
- **gemma2-9b-it** (Google's lightweight model)

## Project Structure

```
ai-assistant/
├── main.py              # Main application and UI
├── config.py            # Configuration management
├── api_client.py        # GroqCloud API integration
├── hotkey_manager.py    # Global keyboard shortcuts
├── requirements.txt     # Python dependencies
├── setup.sh            # Automated setup script
├── start_ai_assistant.sh # Startup script
└── README.md           # This file
```

## Configuration

The application stores configuration in `~/.ai_assistant_config.json`:

- API key
- Selected model
- Window position
- Theme preferences

## Troubleshooting

### Permission Issues
If you get permission errors with keyboard shortcuts:
```bash
# Add your user to the input group (may require restart)
sudo usermod -a -G input $USER
```

### Tkinter Not Found
```bash
sudo apt install python3-tk
```

### Application Won't Start
```bash
# Ensure virtual environment is activated
source venv/bin/activate
python run.py
```

## Keyboard Shortcuts

- **Alt+A**: Toggle AI window
- **Escape**: Hide window (when open)
- **Enter**: Send message (in input field)

## System Requirements

- Ubuntu 22.04+ / Debian 11+
- Python 3.9+
- 2GB RAM minimum
- 100MB disk space

## License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues and enhancement requests.

---

**Enjoy your AI assistant! 🚀**
