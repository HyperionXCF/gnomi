import threading
import queue
import time
from groq import Groq
from typing import List, Dict, Optional


class GroqClient:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.models_cache = []
        self.last_cache_update = 0
        self.cache_duration = 3600  # 1 hour

    def get_available_models(self) -> List[str]:
        current_time = time.time()
        if (
            self.models_cache
            and current_time - self.last_cache_update < self.cache_duration
        ):
            return self.models_cache

        try:
            models = self.client.models.list()
            available_models = []

            # Filter for chat models that are commonly available
            preferred_models = [
                "llama-3.1-8b-instant",
                "llama-3.1-70b-versatile",
                "mixtral-8x7b-32768",
                "gemma2-9b-it",
            ]

            for model in models.data:
                model_id = model.id
                if any(pref in model_id for pref in preferred_models):
                    available_models.append(model_id)

            # Sort by preference
            def get_preference_rank(model_id):
                for i, pref in enumerate(preferred_models):
                    if pref in model_id:
                        return i
                return len(preferred_models)

            available_models.sort(key=get_preference_rank)

            self.models_cache = available_models
            self.last_cache_update = current_time
            return available_models

        except Exception:
            # Fallback to preferred models
            return [
                "llama-3.1-8b-instant",
                "llama-3.1-70b-versatile",
                "mixtral-8x7b-32768",
                "gemma2-9b-it",
            ]

    def chat_completion(
        self,
        messages: List[Dict],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> Optional[str]:
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"


class AsyncGroqClient:
    def __init__(self, api_key: str):
        self.groq_client = GroqClient(api_key)
        self.request_queue = queue.Queue()
        self.response_queue = queue.Queue()
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()

    def _worker(self):
        while True:
            request_data = None
            try:
                request_data = self.request_queue.get()
                request_id, messages, model, temperature, max_tokens = request_data
                response = self.groq_client.chat_completion(
                    messages, model, temperature, max_tokens
                )
                self.response_queue.put((request_id, response))
            except Exception as e:
                # If request extraction fails, use None as request_id
                request_id = request_data[0] if request_data else None
                self.response_queue.put((request_id, f"Error: {str(e)}"))

    def chat_completion(
        self,
        messages: List[Dict],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        callback=None,
    ):
        request_id = id(messages)
        self.request_queue.put((request_id, messages, model, temperature, max_tokens))

        if callback:

            def check_response():
                try:
                    while True:
                        try:
                            rid, response = self.response_queue.get(timeout=0.1)
                            if rid == request_id:
                                callback(response)
                                break
                        except queue.Empty:
                            continue
                except Exception:
                    callback("Error: Failed to get response")

            threading.Thread(target=check_response, daemon=True).start()
