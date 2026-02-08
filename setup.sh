#!/bin/bash

echo "🤖 AI Assistant Setup Script"
echo "============================"

# Check if running on Ubuntu/Debian
if ! command -v apt &> /dev/null; then
    echo "❌ This setup script is designed for Ubuntu/Debian systems."
    echo "   Please install the required packages manually:"
    echo "   - Python 3 with tkinter"
    echo "   - pip"
    exit 1
fi

echo "📦 Installing system dependencies..."
echo "   You may be asked for your password to install packages."

# Install system dependencies
sudo apt update
sudo apt install -y python3 python3-tk python3-pip python3-venv

echo "🐍 Setting up Python virtual environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment and install Python packages
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "🚀 Creating startup scripts..."

# Create startup script
cat > start_ai_assistant.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python run.py
EOF

chmod +x start_ai_assistant.sh

echo "✅ Setup complete!"
echo ""
echo "📋 Usage:"
echo "   1. Run: ./start_ai_assistant.sh"
echo "   2. Press Alt+A to toggle the AI window"
echo "   3. First time: Enter your GroqCloud API key"
echo "   4. Start chatting with AI!"
echo ""
echo "🔑 Get your API key from: https://console.groq.com/"