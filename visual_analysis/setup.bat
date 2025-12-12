@echo off

REM Setup script for video analysis with Qwen3-VL model

echo Setting up video analysis environment...

REM Create virtual environment
python -m venv video_env

REM Activate virtual environment
call video_env\Scripts\activate

REM Upgrade pip
pip install --upgrade pip

REM Install required packages
pip install torch transformers accelerate opencv-python pillow numpy tqdm

echo Environment setup complete!
echo To activate the environment, run: video_env\Scripts\activate