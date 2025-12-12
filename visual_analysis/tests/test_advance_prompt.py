"""
Image Analysis Test with Advanced ComfyUI-Ready Prompt
Tests the enhanced 8-point analysis prompt designed for AI image generation reproduction.

Usage:
    python visual_analysis/tests/test_advance_prompt.py <image_path>
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from visual_analysis.src.ollama_client import OllamaClient


def main():
    if len(sys.argv) < 2:
        print("Usage: python test_advance_prompt.py <image_path>")
        print("\nExample:")
        print("  python visual_analysis/tests/test_advance_prompt.py visual_analysis/data/Goku1024.png")
        sys.exit(1)

    image_path = sys.argv[1]

    if not os.path.exists(image_path):
        print(f"Error: Image not found: {image_path}")
        sys.exit(1)

    # Initialize client with explicit model
    client = OllamaClient(model='qwen3-vl-8b-ctx32k-explicit:latest')

    # Enhanced prompt for ComfyUI reproduction (v3 from PROMPT_TEMPLATES.md)
    prompt = """Analyze this image with extreme detail for image generation purposes:

1. PEOPLE & SUBJECTS:
   - Count and identification (number, primary subjects)
   - Physical appearance: age range, gender, ethnicity, body type (slender/athletic/muscular/curvy/overweight)
   - Facial features: face shape, eyes, nose, mouth, skin tone, distinguishing marks
   - Hair: color, style, length, texture
   - Clothing: style, colors, materials, fit, accessories
   - Pose & positioning: body orientation, limb placement, stance
   - Expression & emotion: facial expression, eye direction, mood conveyed
   - Interactions: with other subjects, with environment, with objects

2. ENVIRONMENT & SETTING:
   - Location type: indoor/outdoor, specific setting (café, forest, studio, street, etc.)
   - Background elements: architecture, furniture, natural features, props
   - Spatial depth: foreground, midground, background separation
   - Color palette: dominant colors, accent colors, color harmony/contrast
   - Textures: materials visible (wood, metal, fabric, glass, etc.)
   - Atmosphere: mood, time of day, weather conditions

3. ACTIONS & DYNAMICS:
   - Primary action: what the main subject is doing
   - Secondary actions: supporting movements or activities
   - Object interactions: items being held, used, or manipulated
   - Motion indicators: blur, frozen action, implied movement

4. IMAGE STYLE & ARTISTIC TREATMENT:
   - Visual medium: photograph/digital art/painting/3D render/anime/sketch
   - Art style: photorealistic, hyperrealistic, stylized, abstract, impressionistic
   - Color grading: warm/cool tones, saturation level, contrast level
   - Post-processing: filters, color adjustments, vignetting
   - Texture quality: smooth/textured, clean/grungy, pristine/weathered

5. CAMERA & COMPOSITION:
   - Shot type: extreme wide/wide/full/medium/close-up/extreme close-up
   - Camera angle: eye-level/high-angle/low-angle/Dutch angle
   - Focal length: ultra-wide/wide/normal/telephoto
   - Depth of field: deep focus/shallow focus, bokeh characteristics
   - Composition: rule of thirds, symmetry, leading lines, framing

6. CAMERA TECHNICAL:
   - Motion: static/panning/tilting/tracking
   - Stability: tripod-stable/handheld/gimbal-smooth
   - Motion blur: frozen/slight blur/heavy blur
   - Focus: sharp throughout/selective focus

7. LIGHTING SETUP:
   - Light type: natural/studio/LED/practical/mixed
   - Time of day: golden hour/blue hour/midday/night
   - Direction: front-lit/side-lit/backlit/rim-lit/top-lit
   - Quality: hard light/soft light
   - Intensity: bright/moderate/dim/high-contrast/low-contrast
   - Color temperature: warm (2700K)/neutral (5000K)/cool (6500K)
   - Shadows: deep/soft, direction
   - Highlights: specular/diffused

8. COMFYUI REPRODUCTION GUIDE:
   - Suggested prompt keywords for recreation
   - Negative prompt suggestions
   - Style reference tags (artist names, art movements)
   - Recommended AI model (SD 1.5/SDXL/Flux)
   - CFG scale recommendation (1-20)
   - Sampling steps recommendation (20-50)

Provide comprehensive analysis for accurate style recreation in AI image generation tools."""

    print(f"Testing Advanced ComfyUI-Ready Prompt")
    print(f"Image: {image_path}")
    print(f"Model: {client.model}")
    print(f"\nProcessing with enhanced 8-point analysis...\n")

    result = client.generate(
        prompt, 
        image_path=image_path, 
        max_tokens=4000,  # Higher token limit for detailed analysis
        debug=False
    )

    print("=" * 70)
    print("ADVANCED ANALYSIS RESULT (ComfyUI-Ready)")
    print("=" * 70)
    print(result)
    print("=" * 70)

    # Save to results folder
    import json
    image_basename = os.path.splitext(os.path.basename(image_path))[0]
    results_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
    os.makedirs(results_dir, exist_ok=True)
    output_path = os.path.join(results_dir, f"{image_basename}_advanced_analysis.json")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            "image": image_path, 
            "model": client.model, 
            "prompt_version": "v3_comfyui_ready",
            "analysis": result
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Advanced analysis saved to: {output_path}")
    print("✓ Analysis complete! Use this for ComfyUI prompt generation.")


if __name__ == "__main__":
    main()
