# Image Analysis Prompt Templates

## Advanced Analysis Prompt (Current - v2)
For detailed analysis with all attributes needed for reproduction in ComfyUI/Stable Diffusion.

### Full 7-Point Analysis
```
Analyze this image in detail:

1. People: Who is present? Describe appearance, clothing, pose, expression, body language, age, gender, ethnicity, physical body type (e.g., slender, muscular, overweight) and emotional state.

2. Environment: Location, setting, background, lighting, color palette, atmosphere.

3. Actions: What's happening? Primary actions, interactions, objects in use.

4. Image Style: Visual style (photorealistic/anime/3D render/painting/etc.), art medium, aesthetic genre, color grading, texture quality.

5. Camera: Shot type (wide/medium/close-up), angle (eye-level/high/low), depth of field, composition.

6. Camera Movement: Static or moving? Any panning/tilting/zooming/tracking? Stability and motion blur.

7. Lighting: Type (natural/artificial), direction, intensity, shadows, highlights, color temperature.

Provide clear, specific descriptions.
```

---

## Enhanced ComfyUI-Ready Prompt (v3 - Recommended)
This version extracts all details needed to recreate the image style in ComfyUI/Stable Diffusion.

### Ultra-Detailed Analysis for Image Generation
```
Analyze this image with extreme detail for image generation purposes:

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
   - Environmental lighting: natural light sources, artificial fixtures

3. ACTIONS & DYNAMICS:
   - Primary action: what the main subject is doing
   - Secondary actions: supporting movements or activities
   - Object interactions: items being held, used, or manipulated
   - Motion indicators: blur, frozen action, implied movement
   - Narrative context: story being told, moment captured

4. IMAGE STYLE & ARTISTIC TREATMENT:
   - Visual medium: photograph/digital art/painting/3D render/anime/sketch
   - Art style: photorealistic, hyperrealistic, stylized, abstract, impressionistic
   - Rendering quality: sharp/soft, detailed/simplified, polished/rough
   - Color grading: warm/cool tones, saturation level, contrast level
   - Film stock simulation: digital/film look, grain, vintage effects
   - Post-processing: filters, color adjustments, vignetting, chromatic aberration
   - Texture quality: smooth/textured, clean/grungy, pristine/weathered
   - Line work: if applicable (comic style, lineart, cel-shading)

5. CAMERA & COMPOSITION:
   - Shot type: extreme wide/wide/full/medium/close-up/extreme close-up
   - Camera angle: eye-level/high-angle/low-angle/Dutch angle/bird's-eye/worm's-eye
   - Focal length equivalence: ultra-wide (14-24mm)/wide (24-35mm)/normal (35-70mm)/telephoto (70-200mm)/super-telephoto (200mm+)
   - Depth of field: deep focus/shallow focus, bokeh characteristics
   - Composition rules: rule of thirds, golden ratio, centered, symmetry, leading lines
   - Framing: tight/loose, negative space usage, aspect ratio
   - Perspective: linear perspective, compression, distortion

6. CAMERA TECHNICAL SETTINGS (if identifiable):
   - Motion: static/panning/tilting/tracking/dolly/crane
   - Stability: tripod-stable/handheld/gimbal-smooth/intentional shake
   - Motion blur: frozen/slight blur/heavy blur
   - Focus: sharp throughout/selective focus/rack focus
   - Image quality: crisp/soft, noise/grain level

7. LIGHTING SETUP:
   - Light type: natural sunlight/window light/studio strobe/continuous LED/practical lights/mixed
   - Time of day: golden hour/blue hour/midday/overcast/night
   - Direction: front-lit/side-lit/backlit/rim-lit/top-lit/under-lit
   - Quality: hard light (harsh shadows)/soft light (diffused shadows)
   - Intensity: bright/moderate/dim/high-contrast/low-contrast
   - Color temperature: warm (2700-3500K)/neutral (4000-5000K)/cool (5500-7000K)/mixed temperatures
   - Shadows: deep/soft, direction, coverage
   - Highlights: specular/diffused, blown-out/retained detail
   - Light ratios: high-key (bright, minimal shadows)/low-key (dramatic, deep shadows)/medium
   - Fill light: present/absent, intensity relative to key light
   - Catch lights: in eyes, reflection patterns

8. TECHNICAL METADATA (for ComfyUI reproduction):
   - Suggested prompt keywords: [extract key descriptive terms]
   - Negative prompt suggestions: [what to avoid]
   - Style reference tags: [artist names, art movements, visual references]
   - Recommended models: [SD 1.5/SDXL/Flux/etc.]
   - Suggested samplers: [DPM++/Euler/etc.]
   - CFG scale recommendation: [numerical guidance]
   - Steps recommendation: [iteration count]
   - LoRA/embedding suggestions: [if specific style detected]

Provide a comprehensive analysis that would allow accurate recreation of this image's style, composition, and mood in an AI image generation tool.
```

---

## Video Frame Analysis Prompt (Current)
Lighter version for video frame analysis (performance-optimized).

```
Analyze this video frame and describe:
1. People present (number, age, gender, clothing)
2. Environment (indoor/outdoor, setting, lighting)
3. Actions being performed
4. Camera style (wide shot, close-up, etc.)
5. Camera movement (pan, zoom, shake, etc.)

Be concise and specific in your descriptions.
```

---

## Usage Notes

### For Image Analysis (Full Detail):
Use **Enhanced ComfyUI-Ready Prompt (v3)** when:
- You need to recreate the image style in ComfyUI/Stable Diffusion
- Analyzing reference images for art direction
- Building a dataset for style transfer
- Need maximum detail extraction

### For Quick Analysis:
Use **Advanced Analysis Prompt (v2)** when:
- You need comprehensive but concise analysis
- Processing many images quickly
- Don't need ComfyUI-specific metadata

### For Video Analysis:
Use **Video Frame Analysis Prompt** when:
- Analyzing video frames in bulk
- Need faster processing
- Focus on temporal/motion aspects

---

## ComfyUI Integration Example

After getting analysis from v3 prompt, extract:

**Positive Prompt:**
```
[People description], [clothing details], [pose], [environment], [style keywords], 
[lighting setup], [camera angle], [artistic treatment], masterpiece, high quality
```

**Negative Prompt:**
```
[Issues detected in analysis], low quality, blurry, distorted, artificial, generic
```

**Settings:**
- Model: Based on style (realistic → SDXL, anime → Animagine, etc.)
- CFG: 7-12 for realistic, 5-8 for artistic
- Steps: 25-40
- Sampler: DPM++ 2M Karras or Euler A
