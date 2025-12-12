"""
Image Analysis CLI using Qwen3-VL via Ollama
Analyzes images to describe people, environment, actions, style, camera, lighting.

Usage:
    python visual_analysis/src/analyze_image_cli.py image.jpg
    python visual_analysis/src/analyze_image_cli.py image.jpg qwen3-vl-8b-ctx32k:latest
"""
import sys
import os
import json

from .ollama_client import OllamaClient


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_image_cli.py <image_path> [model_name]")
        print("\nExamples:")
        print("  python visual_analysis/src/analyze_image_cli.py data/image.jpg")
        print("  python video_analysis/src/analyze_image_cli.py data/image.jpg qwen3-vl-8b-ctx32k:latest")
        sys.exit(1)

    image_path = sys.argv[1]
    model_name = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.exists(image_path):
        print(f"Error: Image not found: {image_path}")
        sys.exit(1)

    # Load model name from config if not provided
    if model_name is None:
        config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                model_name = cfg.get("model", {}).get("name", "qwen3-vl-8b-ctx32k-explicit:latest")
        else:
            model_name = "qwen3-vl-8b-ctx32k-explicit:latest"

    client = OllamaClient(model=model_name)

    prompt = """Analyze this image in detail:

1. People: Who is present? Describe appearance, clothing, pose, expression, body language, age, gender, ethnicity, physical body type (e.g., slender, muscular, overweight) and emotional state.

2. Environment: Location, setting, background, lighting, color palette, atmosphere.

3. Actions: What's happening? Primary actions, interactions, objects in use.

4. Image Style: Visual style (photorealistic/anime/3D render/painting/etc.), art medium, aesthetic genre, color grading, texture quality.

5. Camera: Shot type (wide/medium/close-up), angle (eye-level/high/low), depth of field, composition.

6. Camera Movement: Static or moving? Any panning/tilting/zooming/tracking? Stability and motion blur.

7. Lighting: Type (natural/artificial), direction, intensity, shadows, highlights, color temperature.

Provide clear, specific descriptions."""

    print(f"Analyzing: {image_path}")
    print(f"Using model: {client.model}")
    print(f"HTTP available: {client.http_available()}")
    print("\nProcessing...\n")

    result = client.generate(
        prompt, 
        image_path=image_path, 
        max_tokens=3000,
        debug=False
    )

    print("=" * 70)
    print("ANALYSIS RESULT")
    print("=" * 70)
    print(result)
    print("=" * 70)

    if "<error>" in result or "<ollama-cli-error>" in result:
        print("\nAnalysis failed. Check that Ollama is running and the model is loaded.")
        sys.exit(1)
    else:
        # Save result to JSON file
        image_basename = os.path.splitext(os.path.basename(image_path))[0]
        results_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
        os.makedirs(results_dir, exist_ok=True)
        output_path = os.path.join(results_dir, f"{image_basename}_analysis.json")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({"image": image_path, "model": model_name, "analysis": result}, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Results saved to: {output_path}")
        print("✓ Analysis completed successfully!")


if __name__ == "__main__":
    main()
