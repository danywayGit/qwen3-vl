"""
Test Qwen3-VL-Instruct with official recommended sampling parameters
Based on: https://huggingface.co/Qwen/Qwen3-VL-32B-Instruct
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from visual_analysis.src.ollama_client import OllamaClient

# Initialize with exact model name
client = OllamaClient(model="qwen3-vl-8b-ctx32k:latest")

# Detailed but focused prompt (structured 5-point analysis)
prompt = """Analyze this image and provide:

1. People: Who is present? Describe appearance, clothing, pose, expression.

2. Environment: Location, setting, background, lighting, atmosphere.

3. Actions: What's happening? Primary actions or activities visible.

4. Visual Style: Art style (anime/photorealistic/3D/etc.), aesthetic, color palette.

5. Camera: Shot type, angle, composition, focus.

Provide clear, specific descriptions for each point."""

print("Testing Qwen3-VL-Instruct with official hyperparameters")
print(f"Model: {client.model}")
print("Parameters: temp=0.7, top_p=0.8, top_k=20, presence_penalty=1.5")
print(f"Image: video_analysis/data/Goku1024.png\n")

# Generate with official Qwen3-VL-Instruct parameters (now set in client)
result = client.generate(
    prompt=prompt,
    image_path="video_analysis/data/Goku1024.png",
    max_tokens=2000,  # Reasonable for 5-point analysis
    debug=False
)

print("="*80)
print("RESULT:")
print("="*80)
print(result)
print("="*80)
