"""
Simple Ollama client with HTTP + CLI fallback.

This client attempts to call a local Ollama HTTP endpoint (default http://127.0.0.1:11434)
and falls back to the `ollama` CLI if HTTP isn't available.

Note: image handling via Ollama HTTP may depend on your local Ollama server's expectations.
This implementation sends the image as base64 under the `image_base64` key in JSON.
If your Ollama instance expects a different format, we can adapt this quickly.
"""

import base64
import json
import os
import subprocess
from typing import Optional

import requests


class OllamaClient:
    def __init__(self, model: str = "qwen3-vl-8b-ctx32k:latest", base_url: str = "http://127.0.0.1:11434"):
        self.model = model
        self.base_url = base_url.rstrip("/")

    def _try_endpoints(self):
        # Ollama API endpoints (try chat first as it works better with vision models)
        return [
            "/api/chat",
            "/api/generate",
        ]

    def http_available(self, timeout: float = 1.0) -> bool:
        try:
            url = f"{self.base_url}/"  # simple ping
            r = requests.get(url, timeout=timeout)
            return True
        except Exception:
            return False

    def _post_try(self, chat_payload: dict, generate_payload: dict, timeout: float = 300.0, debug: bool = False) -> Optional[requests.Response]:
        for p in self._try_endpoints():
            try:
                url = f"{self.base_url}{p}"
                # Use appropriate payload for endpoint
                payload = chat_payload if "chat" in p else generate_payload
                r = requests.post(url, json=payload, timeout=timeout, stream=False)
                if debug:
                    print(f"DEBUG: POST {url}")
                    print(f"DEBUG: Status {r.status_code}")
                    print(f"DEBUG: Response: {r.text[:500]}")
                if r.status_code == 200:
                    return r
            except Exception as e:
                if debug:
                    print(f"DEBUG: Exception at {p}: {e}")
                continue
        return None

    def generate(self, prompt: str, image_path: Optional[str] = None, max_tokens: Optional[int] = None, 
                 debug: bool = False) -> str:
        # Load image as base64 if provided
        image_b64 = None
        if image_path is not None and os.path.exists(image_path):
            with open(image_path, "rb") as f:
                b = f.read()
            image_b64 = base64.b64encode(b).decode("ascii")
        
        # Build options with optimal Qwen3-VL sampling parameters
        # Based on official docs: https://huggingface.co/Qwen/Qwen3-VL-32B-Instruct
        options = {}
        if max_tokens is not None:
            options["num_predict"] = max_tokens
        
        # Qwen3-VL-Instruct optimal parameters for vision-language tasks:
        # temperature=0.7, top_p=0.8, top_k=20, presence_penalty=1.5
        options["temperature"] = 0.7
        options["top_p"] = 0.8
        options["top_k"] = 20
        options["presence_penalty"] = 1.5  # Reduces repetition in responses
        
        # Try /api/chat format first (works better with vision models)
        chat_payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False
        }
        if image_b64:
            chat_payload["messages"][0]["images"] = [image_b64]
        if options:
            chat_payload["options"] = options
        
        # Build /api/generate format as fallback
        generate_payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        if image_b64:
            generate_payload["images"] = [image_b64]
        if options:
            generate_payload["options"] = options
        
        # Choose payload based on endpoint
        payload = chat_payload  # Try chat first

        if debug:
            print(f"DEBUG: Chat payload keys: {list(chat_payload.keys())}")
            if image_b64:
                print(f"DEBUG: Image base64 length: {len(image_b64)}")

        # Try HTTP API first
        if self.http_available():
            try:
                r = self._post_try(chat_payload, generate_payload, debug=debug)
                if r is not None:
                    # Parse Ollama response format
                    try:
                        j = r.json()
                        if debug:
                            print(f"DEBUG: Response JSON keys: {list(j.keys())}")
                            print(f"DEBUG: Full response: {j}")
                        
                        # Ollama returns 'response' key for /api/generate
                        if "response" in j and j["response"]:
                            return str(j["response"])
                        
                        # Qwen3-VL models may use 'thinking' field for reasoning (in generate endpoint)
                        if "thinking" in j and j["thinking"]:
                            return str(j["thinking"])
                        
                        # For /api/chat, check 'message' -> 'content' or 'thinking'
                        if "message" in j:
                            msg = j["message"]
                            # Check content first
                            if "content" in msg and msg["content"]:
                                return str(msg["content"])
                            # Check thinking field (Qwen3-VL specific)
                            if "thinking" in msg and msg["thinking"]:
                                return str(msg["thinking"])
                        
                        # Fallback to full JSON
                        return json.dumps(j)
                    except Exception as e:
                        return f"<json-parse-error> {str(e)}: {r.text[:500]}"
            except Exception as e:
                pass

        # Fallback to CLI `ollama run <model>` if available
        try:
            cli_cmd = ["ollama", "run", self.model]
            # send prompt via stdin
            proc = subprocess.run(cli_cmd, input=prompt.encode("utf-8"), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
            if proc.returncode == 0:
                out = proc.stdout.decode("utf-8", errors="ignore")
                return out
            else:
                err = proc.stderr.decode("utf-8", errors="ignore")
                return f"<ollama-cli-error> {err}"
        except FileNotFoundError:
            return "<error> Ollama HTTP not available and `ollama` CLI not found."
        except Exception as e:
            return f"<error> {str(e)}"


if __name__ == "__main__":
    c = OllamaClient()
    print("HTTP available:", c.http_available())
    print(c.generate("Say hello"))
