from pynput import keyboard
import threading
import time


class HotkeyManager:
    def __init__(self, toggle_callback):
        self.toggle_callback = toggle_callback
        self.listener = None
        self.running = False
        self.last_toggle_time = 0
        self.debounce_time = 0.3  # Prevent rapid toggling

    def start(self):
        if self.running:
            return

        self.running = True
        self.listener = keyboard.GlobalHotKeys({"<alt>+<a>": self._on_toggle})
        self.listener.start()

    def stop(self):
        if not self.running:
            return

        self.running = False
        if self.listener:
            self.listener.stop()

    def _on_toggle(self):
        current_time = time.time()
        if current_time - self.last_toggle_time > self.debounce_time:
            self.last_toggle_time = current_time
            self.toggle_callback()
