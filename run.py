#!/usr/bin/env python3

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import AIAssistantUI

if __name__ == "__main__":
    try:
        app = AIAssistantUI()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)
