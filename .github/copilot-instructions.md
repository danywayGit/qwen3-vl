# GitHub Copilot Instructions for qwen3-vl Project

## Project Overview
Video and image analysis tool using Qwen3-VL vision-language model via Ollama HTTP API. Analyzes visual content to describe people, environment, actions, camera style, and camera movement.

## Critical Rules

### Python Environment
- **ALWAYS use virtual environment**: `.venv` in project root
- **Never install packages globally**: All dependencies go in `.venv`
- **Activation required**: Ensure `.venv` is activated before running any Python commands
- **Package installation**: Use `pip install` only within activated `.venv`

### Model Management
- **Models are managed externally**: All Ollama model definitions and Modelfiles are in the `OllamaTools` repository
- **Do NOT create Modelfiles here**: Never generate or modify Ollama Modelfile configurations in this repo
- **Model references only**: Only reference model names (e.g., `qwen3-vl-8b-ctx32k-explicit:latest`)
- **config.json**: Update model name in `visual_analysis/config.json` to switch models

### Architecture Principles
- **Ollama HTTP API**: Use `/api/chat` endpoint (not `/api/generate`)
- **Response parsing**: Qwen3-VL returns output in `"thinking"` field of JSON response
- **No HuggingFace**: This project uses Ollama exclusively, not transformers/torch directly
- **Config-driven**: Read settings from `visual_analysis/config.json` when possible

## Project Structure
```
qwen3-vl/
├── .venv/                    # Virtual environment (REQUIRED, gitignored)
├── requirements.txt          # Python dependencies
└── visual_analysis/
    ├── config.json           # Model & analysis settings
    ├── data/                 # Sample images/videos (gitignored)
    ├── results/              # Analysis outputs (gitignored for privacy)
    ├── src/
    │   ├── ollama_client.py     # Ollama HTTP client
    │   ├── analyze_image_cli.py # Image analysis (standalone CLI)
    │   └── analyze_video_cli.py # Video analysis (standalone CLI)
    └── tests/
```

## Code Guidelines

### When Writing Python Code
1. **Import with relative imports**: CLI files use `from .ollama_client import OllamaClient`
2. **Read config.json**: VideoAnalyzer class reads model name from config if not provided
3. **Error handling**: Always wrap Ollama API calls in try-except
4. **Type hints**: Use type hints for function parameters and returns
5. **Docstrings**: Include docstrings for all public functions/classes

### Model Configuration
```python
# CORRECT: Read from config.json (in analyze_video_cli.py)
analyzer = VideoAnalyzer(model_name=None)

# CORRECT: Override with specific model
analyzer = VideoAnalyzer(model_name="qwen3-vl-8b-ctx32k-explicit:latest")

# WRONG: Don't hardcode old model names
analyzer = VideoAnalyzer(model_name="qwen3-vl-32b-ctx128k:latest")
```

### File Organization
- **CLI files** (`analyze_image_cli.py`, `analyze_video_cli.py`): Standalone, include all logic
- **VideoAnalyzer class**: Embedded in `analyze_video_cli.py` (not separate file)
- **Output location**: All results auto-saved to `visual_analysis/results/` (gitignored for privacy)
- **Data files**: Videos/images in `visual_analysis/data/` (gitignored, too large)
- **Virtual env name**: Always use `.venv` (not `venv` or `env`)

### Ollama Client Usage
```python
from visual_analysis.src.ollama_client import OllamaClient

client = OllamaClient(model='qwen3-vl-8b-ctx32k-explicit:latest')
response = client.generate(
    prompt="Analyze this image...",
    image_path="path/to/image.jpg",
    max_tokens=3000,
    debug=False
)
```

## Performance Expectations (RTX 4090)
- **8B model**: ~3-4s per image, ~21GB GPU usage
- **32K context**: Optimal balance (enough for detailed analysis)
- **128K context**: Overkill, slower, no quality benefit for images
- **Video analysis**: ~3-4s per frame

## Testing Strategy
- **Quick test**: `python visual_analysis/tests/test_quick.py` (1-sentence output)
- **Detailed test**: `python visual_analysis/tests/test_detailed.py` (6-point analysis)
- **Image CLI**: `python -m visual_analysis.src.analyze_image_cli visual_analysis/data/Goku1024.png`
- **Video CLI**: `python -m visual_analysis.src.analyze_video_cli video.mp4 --start 1:05 --end 2:45`

## Common Tasks

### Adding New Analysis Features
1. Update prompt in `analyze_image_cli.py` or `analyze_video_cli.py`
2. Modify `VideoAnalyzer.analyze_video()` if frame processing changes
3. Test with sample images/videos in `visual_analysis/data/`

### Changing Models
1. **Do NOT modify this repo**: Update model in `OllamaTools` repo
2. Update `visual_analysis/config.json` with new model name
3. Test with `python analyze_image.py <test_image>`

### Adding Dependencies
```powershell
# ALWAYS activate venv first
.venv\Scripts\activate

# Install new package
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt
```

## Anti-Patterns to Avoid
❌ Installing packages without `.venv` activation  
❌ Creating Modelfiles in this repository  
❌ Hardcoding model names in source code  
❌ Using HuggingFace transformers instead of Ollama  
❌ Ignoring config.json and duplicating settings  
❌ Using `/api/generate` endpoint (use `/api/chat`)  
❌ Parsing `"response"` field (use `"thinking"` for Qwen3-VL)  

## Best Practices
✅ Use virtual environment for all Python operations  
✅ Reference models by name only (definitions in OllamaTools)  
✅ Read settings from config.json when available  
✅ Use Ollama HTTP API with `/api/chat` endpoint  
✅ Parse `"thinking"` field from Qwen3-VL responses  
✅ Apply official Qwen3-VL-Instruct parameters (temp=0.7, top_p=0.8, top_k=20)  
✅ Test with sample data before running on large videos  

## Related Repositories
- **OllamaTools**: Model definitions, Modelfiles, context configurations
- **This repo (qwen3-vl)**: Video/image analysis application only

## Hardware Context
- **Target GPU**: NVIDIA RTX 4090 (24GB VRAM)
- **Recommended model**: 8B parameter variant with 32K context
- **Why not 128K**: Creates 17.6GB KV cache, forces layers to CPU, no quality benefit
