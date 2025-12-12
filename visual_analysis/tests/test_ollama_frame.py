"""
Test script for Ollama local model with an image payload.

Uses the OllamaClient to test the HTTP API with a sample image.
"""
import os
import sys

# Add parent dir to path to import ollama_client
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from visual_analysis.src.ollama_client import OllamaClient
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(ROOT, 'data')
os.makedirs(DATA_DIR, exist_ok=True)
SAMPLE_PATH = os.path.join(DATA_DIR, 'sample_frame.png')

# Create a simple gradient image
W, H = 64, 48
img = Image.new('RGB', (W, H))
pixels = img.load()
for y in range(H):
    for x in range(W):
        r = int((x / (W - 1)) * 255)
        g = int((y / (H - 1)) * 255)
        b = int(((x + y) / (W + H - 2)) * 255)
        pixels[x, y] = (r, g, b)
img.save(SAMPLE_PATH)

print(f"Created test image: {SAMPLE_PATH}")

# Initialize client (will read model from config.json)
client = OllamaClient(model="qwen3-vl-32b-ctx128k:latest")

print(f"Using model: {client.model}")
print(f"HTTP available: {client.http_available()}")

# Test with image
prompt = "Describe this image briefly."
print(f"\nSending prompt with image to Ollama...")
response = client.generate(prompt, image_path=SAMPLE_PATH, max_tokens=100)

print(f"\n{'='*60}")
print("OLLAMA RESPONSE:")
print('='*60)
print(response)
print('='*60)

if "<error>" in response or "<ollama-cli-error>" in response:
    print("\nTest failed. Check that Ollama is running and the model is loaded.")
    sys.exit(1)
else:
    print("\nTest completed successfully!")
    sys.exit(0)
