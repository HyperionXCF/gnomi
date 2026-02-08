import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
import threading
import time
from typing import Optional, List, Dict
from config import Config
from api_client import AsyncGroqClient
from hotkey_manager import HotkeyManager


class AIAssistantUI:
    def __init__(self):
        self.config = Config()
        self.root = tk.Tk()
        self.groq_client: Optional[AsyncGroqClient] = None
        self.hotkey_manager = HotkeyManager(self.toggle_window)
        self.is_visible = False
        self.is_processing = False

        self._setup_window()
        self._setup_styles()
        self._create_widgets()

        if self.config.is_api_key_set():
            self._init_groq_client()
            self._load_models()

    def _setup_window(self):
        self.root.title("AI Assistant")
        self.root.geometry("450x600")
        self.root.configure(bg="#2b2b2b")
        self.root.resizable(True, True)
        self.root.attributes("-topmost", True)

        # Set window icon and initial position
        position = self.config.get("window_position", [100, 100])
        if isinstance(position, list) and len(position) == 2:
            self.root.geometry(f"+{position[0]}+{position[1]}")
        else:
            self.root.geometry("+100+100")

        # Remove window decorations for cleaner look
        self.root.overrideredirect(False)

        # Bind events
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)
        self.root.bind("<Escape>", lambda e: self.hide_window())

        # Make window draggable
        self.root.bind("<Button-1>", self.start_move)
        self.root.bind("<ButtonRelease-1>", self.stop_move)
        self.root.bind("<B1-Motion>", self.on_move)

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Configure dark theme colors
        bg_color = "#2b2b2b"
        fg_color = "#ffffff"
        entry_bg = "#3c3c3c"
        button_bg = "#4a4a4a"
        button_hover = "#5a5a5a"

        self.root.configure(bg=bg_color)

        # Style configuration
        style.configure("Dark.TFrame", background=bg_color)
        style.configure("Dark.TLabel", background=bg_color, foreground=fg_color)
        style.configure(
            "Dark.TButton",
            background=button_bg,
            foreground=fg_color,
            borderwidth=0,
            focuscolor="none",
        )
        style.map("Dark.TButton", background=[("active", button_hover)])
        style.configure(
            "Dark.TEntry",
            fieldbackground=entry_bg,
            foreground=fg_color,
            borderwidth=1,
            relief="flat",
        )
        style.configure(
            "Dark.TCombobox",
            fieldbackground=entry_bg,
            background=button_bg,
            foreground=fg_color,
            borderwidth=1,
            relief="flat",
        )

    def _create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, style="Dark.TFrame", padding="10")
        main_frame.pack(fill="both", expand=True)

        # Title bar
        title_frame = ttk.Frame(main_frame, style="Dark.TFrame")
        title_frame.pack(fill="x", pady=(0, 10))

        title_label = ttk.Label(
            title_frame,
            text="🤖 AI Assistant",
            font=("Arial", 14, "bold"),
            style="Dark.TLabel",
        )
        title_label.pack(side="left")

        settings_btn = ttk.Button(
            title_frame,
            text="⚙",
            command=self.show_settings,
            style="Dark.TButton",
            width=3,
        )
        settings_btn.pack(side="right", padx=(5, 0))

        # Model selection
        model_frame = ttk.Frame(main_frame, style="Dark.TFrame")
        model_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(model_frame, text="Model:", style="Dark.TLabel").pack(side="left")
        self.model_var = tk.StringVar(value=self.config.get("selected_model", ""))
        self.model_combo = ttk.Combobox(
            model_frame,
            textvariable=self.model_var,
            style="Dark.TCombobox",
            state="readonly",
        )
        self.model_combo.pack(side="left", padx=(10, 0), fill="x", expand=True)

        # Chat area
        chat_frame = ttk.Frame(main_frame, style="Dark.TFrame")
        chat_frame.pack(fill="both", expand=True, pady=(0, 10))

        self.chat_area = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            bg="#1e1e1e",
            fg="#ffffff",
            font=("Consolas", 10),
            relief="flat",
            borderwidth=1,
            height=20,
        )
        self.chat_area.pack(fill="both", expand=True)
        self.chat_area.configure(state="disabled")

        # Input area
        input_frame = ttk.Frame(main_frame, style="Dark.TFrame")
        input_frame.pack(fill="x")

        self.input_var = tk.StringVar()
        self.input_entry = ttk.Entry(
            input_frame,
            textvariable=self.input_var,
            style="Dark.TEntry",
            font=("Arial", 11),
        )
        self.input_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.input_entry.bind("<Return>", self.send_message)

        self.send_btn = ttk.Button(
            input_frame,
            text="Send",
            command=self.send_message,
            style="Dark.TButton",
            width=8,
        )
        self.send_btn.pack(side="right")

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            font=("Arial", 8),
            style="Dark.TLabel",
        )
        status_bar.pack(fill="x", pady=(5, 0))

    def start_move(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def stop_move(self, event):
        # Save current position
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        self.config.set("window_position", [x, y])

    def on_move(self, event):
        x = event.x_root - self.start_x
        y = event.y_root - self.start_y
        self.root.geometry(f"+{x}+{y}")

    def _init_groq_client(self):
        api_key = self.config.get("api_key")
        if api_key:
            try:
                self.groq_client = AsyncGroqClient(api_key)
                return True
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Failed to initialize Groq client: {str(e)}"
                )
                return False
        return False

    def _load_models(self):
        if not self.groq_client:
            return

        def load():
            try:
                if self.groq_client and hasattr(self.groq_client, "groq_client"):
                    models = self.groq_client.groq_client.get_available_models()
                else:
                    return
                self.model_combo["values"] = models
                if models and not self.model_var.get():
                    self.model_var.set(models[0])
            except Exception as e:
                print(f"Failed to load models: {e}")

        threading.Thread(target=load, daemon=True).start()

    def show_window(self):
        if not self.is_visible:
            self.is_visible = True
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
            self.input_entry.focus()

    def hide_window(self):
        if self.is_visible:
            self.is_visible = False
            self.root.withdraw()

    def toggle_window(self):
        if self.is_visible:
            self.hide_window()
        else:
            if not self.config.is_api_key_set():
                self.show_settings()
            else:
                self.show_window()

    def send_message(self, event=None):
        if self.is_processing:
            return

        message = self.input_var.get().strip()
        if not message or not self.groq_client:
            return

        self.is_processing = True
        self.send_btn.configure(state="disabled", text="...")
        self.status_var.set("Thinking...")

        # Add user message to chat
        self._add_message("You", message)
        self.input_var.set("")

        # Get AI response
        messages = [{"role": "user", "content": message}]
        model = self.model_var.get()

        def get_response(response_text):
            self._add_message("AI", response_text)
            self.is_processing = False
            self.send_btn.configure(state="normal", text="Send")
            self.status_var.set("Ready")

        self.groq_client.chat_completion(messages, model, callback=get_response)

    def _add_message(self, sender: str, message: str):
        self.chat_area.configure(state="normal")

        # Add timestamp and sender
        timestamp = time.strftime("%H:%M")
        self.chat_area.insert(tk.END, f"[{timestamp}] {sender}:\n", "sender")
        self.chat_area.insert(tk.END, f"{message}\n\n", "message")

        # Configure tags for styling
        self.chat_area.tag_config(
            "sender", font=("Arial", 9, "bold"), foreground="#888888"
        )
        self.chat_area.tag_config("message", font=("Arial", 10))

        self.chat_area.configure(state="disabled")
        self.chat_area.see(tk.END)

    def show_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.configure(bg="#2b2b2b")
        settings_window.transient(self.root)
        settings_window.grab_set()
        settings_window.attributes("-topmost", True)

        # Center the settings window
        settings_window.update_idletasks()
        x = (settings_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (settings_window.winfo_screenheight() // 2) - (300 // 2)
        settings_window.geometry(f"+{x}+{y}")

        main_frame = ttk.Frame(settings_window, style="Dark.TFrame", padding="20")
        main_frame.pack(fill="both", expand=True)

        # API Key section
        ttk.Label(
            main_frame,
            text="GroqCloud API Key:",
            font=("Arial", 11, "bold"),
            style="Dark.TLabel",
        ).pack(anchor="w", pady=(0, 5))

        api_key_var = tk.StringVar(value=self.config.get("api_key", ""))
        api_key_entry = ttk.Entry(
            main_frame, textvariable=api_key_var, style="Dark.TEntry", show="*"
        )
        api_key_entry.pack(fill="x", pady=(0, 10))

        # Instructions
        instructions = (
            "Get your API key from: https://console.groq.com/\n"
            "Create a free account and generate an API key."
        )
        ttk.Label(
            main_frame,
            text=instructions,
            font=("Arial", 9),
            style="Dark.TLabel",
            foreground="#888888",
        ).pack(anchor="w", pady=(0, 20))

        # Buttons
        button_frame = ttk.Frame(main_frame, style="Dark.TFrame")
        button_frame.pack(fill="x")

        def save_settings():
            api_key = api_key_var.get().strip()
            if api_key:
                self.config.set("api_key", api_key)
                self._init_groq_client()
                self._load_models()
                messagebox.showinfo("Success", "API key saved successfully!")
            settings_window.destroy()

        ttk.Button(
            button_frame, text="Save", command=save_settings, style="Dark.TButton"
        ).pack(side="right", padx=(10, 0))
        ttk.Button(
            button_frame,
            text="Cancel",
            command=settings_window.destroy,
            style="Dark.TButton",
        ).pack(side="right")

        # Focus on API key entry
        api_key_entry.focus()

    def run(self):
        # Start hotkey manager
        self.hotkey_manager.start()

        # Initially hide window
        self.hide_window()

        # Start the GUI event loop
        self.root.mainloop()

        # Cleanup
        self.hotkey_manager.stop()


if __name__ == "__main__":
    app = AIAssistantUI()
    app.run()
