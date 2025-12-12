#!/bin/bash

# Setup script for video analysis with Qwen3-VL model

echo "Setting up video analysis environment..."

# Create virtual environment
python -m venv video_env

# Activate virtual environment
source video_env/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install required packages
pip install torch transformers accelerate opencv-python pillow numpy tqdm

echo "Environment setup complete!"
echo "To activate the environment, run: source video_env/bin/activate"