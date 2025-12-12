# Qwen3-VL Video Analysis Setup

Analyzes videos and images using Qwen3-VL via Ollama, providing detailed descriptions of people, environment, actions, camera style, and movement.

## Quick Start

```powershell
# 1. Install Ollama and pull the model
ollama pull qwen3-vl:8b

# 2. Analyze an image
python -m video_analysis.src.analyze_image_cli video_analysis/data/Goku1024.png

# 3. Analyze a video (time range 1:05 to 2:45)
python -m video_analysis.src.analyze_video_cli video_analysis/data/test1.mp4 --start 1:05 --end 2:45 --interval 60
```

## Model Configuration

### Recommended: qwen3-vl-8b-ctx32k (Optimized for RTX 4090)

**Why 8B with 32K context?**
- ✅ **Fits GPU**: ~21GB GPU usage (leaves 3GB headroom on 24GB RTX 4090)
- ✅ **Fast**: 3-4s for images, 30-90s for detailed analysis
- ✅ **Enough context**: 32K tokens is plenty for detailed image descriptions
- ⚠️ **128K context is overkill**: Creates 17.6GB KV cache, forces 9 layers to CPU, slower with no benefit for images

**Performance (RTX 4090):**
```
Model: qwen3-vl-8b-ctx32k:latest
GPU Layers: 28-33/37 (76-89% on GPU)
Speed: 3.5s total (2.6s load + 0.4s generation)
```

### Creating Optimized Model### Official Qwen3-VL-Instruct Parameters
- **temperature**: 0.7
- **top_p**: 0.8
- **top_k**: 20
- **presence_penalty**: 1.5 (reduces repetition)
- **presence_penalty**: 1.5 (reduces repetition)

## Model Comparison for RTX 4090

| Model | Size | Context | GPU Memory | Layers on GPU | Speed | Best For |
|-------|------|---------|------------|---------------|-------|----------|
| **8B-32K** ✅ | 6.1GB | 32K | ~21GB | 28-33/37 | **Fast** | Recommended |
| 8B-128K | 6.1GB | 128K | ~21GB | 28/37 | Slower | Unnecessary |
| 32B-32K | 19GB | 32K | ~40GB | 40/65 | Slow | CPU hybrid |
| 32B-128K | 19GB | 128K | ~55GB | 22/65 | Very slow | Too big |

**Key Finding**: 128K context provides no quality benefit for image analysis but uses 4x more memory and runs slower.

## Project Structure

```
qwen3-vl/
├── .venv/                    # Virtual environment (do not commit)
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── video_analysis/
    ├── config.json           # Model & analysis settings
    ├── data/                 # Sample images/videos (gitignored)
    ├── results/              # Analysis outputs (gitignored for privacy)
    ├── src/
    │   ├── ollama_client.py     # Ollama HTTP client
    │   ├── analyze_image_cli.py # Image analysis CLI
    │   └── analyze_video_cli.py # Video analysis CLI
    └── tests/
        ├── test_quick.py        # Quick test
        └── test_detailed.py     # Detailed test
```

## Configuration

### config.json
The `video_analysis/config.json` file stores default settings:
- **model.name**: Ollama model to use (e.g., `qwen3-vl-8b-ctx32k-explicit:latest`)
- **model.parameters**: Temperature, top_p, top_k, repeat_penalty
- **video_analysis.frame_interval**: Extract every N frames (default: 30)
- **video_analysis.description_fields**: Analysis categories

The VideoAnalyzer automatically reads this file if no model name is provided.

## Usage Examples

### Image Analysis
```powershell
# Basic usage
python -m video_analysis.src.analyze_image_cli path/to/image.jpg

# With specific model
python -m video_analysis.src.analyze_image_cli image.jpg qwen3-vl-8b-ctx32k:latest
```

### Video Analysis
```powershell
# Full video (output auto-saved to video_analysis/results/)
python -m video_analysis.src.analyze_video_cli video.mp4

# Time range (1:05 to 2:45)
python -m video_analysis.src.analyze_video_cli video.mp4 --start 1:05 --end 2:45

# Custom interval (every 120 frames)
python -m video_analysis.src.analyze_video_cli video.mp4 --interval 120

# Specify custom output path
python -m video_analysis.src.analyze_video_cli video.mp4 --output my_analysis.json
```

## Analysis Output

**6-Point Analysis:**
1. **People**: Appearance, clothing, pose, expression, body language
2. **Environment**: Location, setting, background, lighting, atmosphere
3. **Actions**: Activities, interactions, objects in use
4. **Image Style**: Art medium, aesthetic genre, color grading, texture
5. **Camera**: Shot type, angle, depth of field, composition
6. **Camera Movement**: Pan, tilt, zoom, shake, stability

## Hardware Requirements

- **GPU**: NVIDIA RTX 4090 (24GB VRAM) or similar
- **RAM**: 16GB+ system RAM
- **Disk**: ~10GB for model + data

## Ollama Setup Notes

- **Endpoint**: `http://127.0.0.1:11434`
- **API**: `/api/chat` (preferred for vision models)
- **Response Format**: Check `"thinking"` field for Qwen3-VL output
- **Flash Attention**: Enabled automatically by Ollama

## Troubleshooting

**Out of Memory**:
- Use 32K context instead of 128K
- Reduce `frame_interval` for videos
- Consider 2B model for very fast inference

**Slow Performance**:
- Check GPU utilization in Ollama console
- Ensure using 32K context model
- Verify flash attention is enabled

**Model Not Found**:
```powershell
ollama list  # Check available models
ollama pull qwen3-vl:8b  # Download if needed
```

## References

- [Qwen3-VL-32B-Instruct](https://huggingface.co/Qwen/Qwen3-VL-32B-Instruct)
- [Ollama Documentation](https://ollama.ai/)
- [Qwen3 Technical Report](https://arxiv.org/abs/2505.09388)
