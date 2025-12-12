"""
Video Analysis CLI using Qwen3-VL via Ollama
Analyzes videos to describe people, environment, actions, camera style, and camera movement.

Usage:
    python video_analysis/src/analyze_video_cli.py video.mp4
    python video_analysis/src/analyze_video_cli.py video.mp4 --start 1:05 --end 2:45
"""
import sys
import os
import argparse
import json
import cv2
import numpy as np
from PIL import Image
from tqdm import tqdm
import tempfile
from typing import List, Dict, Any

from .ollama_client import OllamaClient


class VideoAnalyzer:
    """Video analyzer using Qwen3-VL via Ollama HTTP API"""
    
    def __init__(self, model_name: str = None, config_path: str = "../config.json", ollama_base_url: str = "http://127.0.0.1:11434"):
        """
        Initialize the video analyzer.

        Args:
            model_name (str|None): Ollama model name. If None, reads from config.json
            config_path (str): Path to config.json
            ollama_base_url (str): Ollama HTTP endpoint
        """
        # Load config
        cfg = None
        cfg_path_full = os.path.join(os.path.dirname(__file__), config_path)
        if os.path.exists(cfg_path_full):
            try:
                with open(cfg_path_full, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
            except Exception:
                cfg = None

        # Get model name
        if model_name is None:
            if cfg and "model" in cfg and "name" in cfg["model"]:
                model_name = cfg["model"]["name"]
        self.model_name = model_name or "qwen3-vl-8b-ctx32k-explicit:latest"

        # Get parameters
        params = {}
        if cfg and "model" in cfg and "parameters" in cfg["model"]:
            params = cfg["model"]["parameters"]
        self.max_new_tokens = params.get("max_new_tokens", 512)

        # Initialize Ollama client
        self.ollama = OllamaClient(model=self.model_name, base_url=ollama_base_url)
        print(f"Using Ollama model: {self.model_name} (HTTP endpoint: {ollama_base_url})")
        
    def extract_frames(self, video_path: str, frame_interval: int = 30, start_time: float = 0, end_time: float = None) -> List[tuple]:
        """Extract frames from video at specified intervals."""
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        start_frame = int(start_time * fps)
        end_frame = int(end_time * fps) if end_time else total_frames
        
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        frames = []
        frame_count = start_frame
        
        while frame_count < end_frame:
            ret, frame = cap.read()
            if not ret:
                break
                
            if (frame_count - start_frame) % frame_interval == 0:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                timestamp = frame_count / fps
                frames.append((frame_rgb, timestamp))
                
            frame_count += 1
            
        cap.release()
        return frames
    
    def analyze_frame(self, frame: np.ndarray) -> str:
        """Analyze a single frame."""
        image = Image.fromarray(frame)

        prompt = (
            "Analyze this video frame and describe:\n"
            "1. People present (number, age, gender, clothing)\n"
            "2. Environment (indoor/outdoor, setting, lighting)\n"
            "3. Actions being performed\n"
            "4. Camera style (wide shot, close-up, etc.)\n"
            "5. Camera movement (pan, zoom, shake, etc.)\n\n"
            "Be concise and specific in your descriptions."
        )

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = tmp.name
            image.save(tmp_path)

        try:
            resp = self.ollama.generate(prompt, image_path=tmp_path, max_tokens=self.max_new_tokens)
        finally:
            try:
                os.remove(tmp_path)
            except Exception:
                pass

        return resp
    
    def analyze_video(self, video_path: str, frame_interval: int = 30, start_time: float = 0, end_time: float = None) -> List[Dict[str, Any]]:
        """Analyze entire video and return frame-by-frame results."""
        print(f"Analyzing video: {video_path}")
        
        print("Extracting frames...")
        frames = self.extract_frames(video_path, frame_interval, start_time, end_time)
        print(f"Extracted {len(frames)} frames")
        
        print("Analyzing frames...")
        frame_analyses = []
        for i, (frame, timestamp) in enumerate(tqdm(frames)):
            analysis = self.analyze_frame(frame)
            frame_analyses.append({
                "frame_number": i + 1,
                "timestamp": round(timestamp, 2),
                "analysis": analysis
            })
        
        return frame_analyses


def parse_time(time_str):
    """Parse time string (mm:ss) to seconds"""
    parts = time_str.split(':')
    if len(parts) == 2:
        return int(parts[0]) * 60 + int(parts[1])
    return int(time_str)


def main():
    parser = argparse.ArgumentParser(description='Analyze video frames using Qwen3-VL')
    parser.add_argument('video_path', help='Path to video file')
    parser.add_argument('--start', default='0:00', help='Start time (mm:ss)')
    parser.add_argument('--end', default=None, help='End time (mm:ss)')
    parser.add_argument('--interval', type=int, default=30, help='Frame interval (default: 30)')
    parser.add_argument('--output', default=None, help='Output JSON path (default: auto)')
    parser.add_argument('--model', default=None, help='Model name (default: from config.json)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.video_path):
        print(f"Error: Video not found: {args.video_path}")
        sys.exit(1)
    
    start_time = parse_time(args.start)
    end_time = parse_time(args.end) if args.end else None
    
    print(f"Video Analysis Configuration:")
    print(f"  Video: {args.video_path}")
    print(f"  Model: {args.model or '(from config.json)'}")
    print(f"  Start: {start_time}s ({args.start})")
    if end_time:
        print(f"  End: {end_time}s ({args.end})")
        print(f"  Duration: {end_time - start_time}s")
    print(f"  Frame interval: every {args.interval} frames")
    print()
    
    analyzer = VideoAnalyzer(model_name=args.model)
    
    if args.output is None:
        video_basename = os.path.splitext(os.path.basename(args.video_path))[0]
        results_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
        os.makedirs(results_dir, exist_ok=True)
        args.output = os.path.join(results_dir, f"{video_basename}_analysis.json")
    
    print("Starting analysis...\n")
    results = analyzer.analyze_video(args.video_path, start_time=start_time, end_time=end_time)
    
    print("\n" + "="*70)
    print("VIDEO ANALYSIS RESULTS")
    print("="*70)
    
    for i, result in enumerate(results, 1):
        print(f"\n--- Frame {i} (Time: {result.get('timestamp', 'N/A')}s) ---")
        print(result.get('analysis', 'No analysis available'))
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Results saved to: {args.output}")
    print(f"✓ Analysis complete! Processed {len(results)} frames.")


if __name__ == "__main__":
    main()
