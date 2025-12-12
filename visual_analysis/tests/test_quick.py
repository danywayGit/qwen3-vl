"""Quick test with minimal prompt"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from visual_analysis.src.ollama_client import OllamaClient

client = OllamaClient(model='qwen3-vl-8b-ctx32k:latest')
response = client.generate("Describe this image in one sentence.", image_path="visual_analysis/data/Goku1024.png", max_tokens=50, debug=True)
print("\n" + "="*60)
print(response)
print("="*60)
