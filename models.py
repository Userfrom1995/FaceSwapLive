"""
Model Management for Face Swap Live
Handles model availability checking and automatic downloading
"""
import os
import requests
from pathlib import Path
import logging
from typing import Tuple, Optional
from config import config

logger = logging.getLogger(__name__)

def log_with_timestamp(message):
    """Enhanced logging with timestamp"""
    from datetime import datetime
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[{timestamp}] {message}")

def debug_log(message):
    """Debug logging for troubleshooting"""
    from datetime import datetime
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[{timestamp}] DEBUG: {message}")

def ensure_models_directory():
    """Ensure models directory exists"""
    models_dir = Path(config.models.MODELS_DIR)
    models_dir.mkdir(exist_ok=True)
    return models_dir

def download_model(url: str, filepath: Path) -> bool:
    """Download a model file from URL"""
    try:
        log_with_timestamp(f"Downloading model: {filepath.name}")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        progress = (downloaded / total_size) * 100
                        print(f"\rProgress: {progress:.1f}%", end='', flush=True)
        
        print()  # New line after progress
        log_with_timestamp(f"Model downloaded successfully: {filepath.name}")
        return True
        
    except Exception as e:
        log_with_timestamp(f"Failed to download {filepath.name}: {e}")
        if filepath.exists():
            filepath.unlink()  # Remove partial download
        return False

def get_best_models() -> Tuple[Optional[str], Optional[str]]:
    """
    Get the best available face swapper and analysis models
    Returns: (face_swapper_path, face_analysis_path)
    """
    models_dir = ensure_models_directory()
    
    # Priority order for face swapper models (based on actual available models)
    face_swapper_models = [
        "inswapper_128.onnx",        # Full precision - best quality
        "inswapper_128_fp16.onnx"    # Half precision - faster, less VRAM
    ]
    
    # Find best available face swapper
    face_swapper_path = None
    for model_name in face_swapper_models:
        model_path = models_dir / model_name
        if model_path.exists() and model_path.stat().st_size > 1000000:  # At least 1MB
            face_swapper_path = str(model_path)
            log_with_timestamp(f"Found face swapper: {model_name}")
            break
    
    # Face analysis model (buffalo_l is downloaded automatically by insightface)
    face_analysis_path = "buffalo_l"  # This will be handled by insightface
    
    return face_swapper_path, face_analysis_path

def ensure_models_available() -> bool:
    """
    Ensure required models are available with smart download strategy
    
    Strategy:
    1. If user has inswapper_128.onnx (best quality) -> use it, download GFPGAN if missing
    2. If user has only inswapper_128_fp16.onnx -> use it, download GFPGAN if missing  
    3. If user has no face swapper -> download inswapper_128.onnx (best quality)
    4. Always ensure GFPGAN is available for enhancement
    
    Returns: True if models are ready, False otherwise
    """
    models_dir = ensure_models_directory()
    
    # Model URLs from instructions.txt
    MODEL_URLS = {
        "inswapper_128.onnx": "https://github.com/Userfrom1995/FaceSwapLive/releases/download/v1.0.0/inswapper_128.onnx",
        "inswapper_128_fp16.onnx": "https://github.com/Userfrom1995/FaceSwapLive/releases/download/v1.0.0/inswapper_128_fp16.onnx", 
        "GFPGANv1.4.pth": "https://github.com/Userfrom1995/FaceSwapLive/releases/download/v1.0.0/GFPGANv1.4.pth"
    }
    
    # Check current model status
    has_full_precision = (models_dir / "inswapper_128.onnx").exists()
    has_fp16 = (models_dir / "inswapper_128_fp16.onnx").exists()
    has_gfpgan = (models_dir / "GFPGANv1.4.pth").exists()
    
    log_with_timestamp("Checking model availability...")
    debug_log(f"Models directory: {models_dir}")
    debug_log(f"Has inswapper_128.onnx: {has_full_precision}")
    debug_log(f"Has inswapper_128_fp16.onnx: {has_fp16}")
    debug_log(f"Has GFPGANv1.4.pth: {has_gfpgan}")
    
    # Scenario 1: User has best model (full precision)
    if has_full_precision:
        log_with_timestamp("Found inswapper_128.onnx (best quality)")
        if not has_gfpgan:
            log_with_timestamp("Downloading GFPGAN for face enhancement...")
            if not download_model(MODEL_URLS["GFPGANv1.4.pth"], models_dir / "GFPGANv1.4.pth"):
                log_with_timestamp("GFPGAN download failed, continuing without enhancement")
        return True
    
    # Scenario 2: User has FP16 model only
    elif has_fp16:
        log_with_timestamp("Found inswapper_128_fp16.onnx (fast, lower VRAM)")
        if not has_gfpgan:
            log_with_timestamp("Downloading GFPGAN for face enhancement...")
            if not download_model(MODEL_URLS["GFPGANv1.4.pth"], models_dir / "GFPGANv1.4.pth"):
                log_with_timestamp("GFPGAN download failed, continuing without enhancement")
        return True
    
    # Scenario 3: User has no face swapper models
    else:
        log_with_timestamp("No face swapper models found")
        log_with_timestamp("Downloading inswapper_128.onnx (best quality)...")
        
        # Download the best model first
        if download_model(MODEL_URLS["inswapper_128.onnx"], models_dir / "inswapper_128.onnx"):
            log_with_timestamp("Face swapper model downloaded successfully")
            
            # Also download GFPGAN
            if not has_gfpgan:
                log_with_timestamp("Downloading GFPGAN for face enhancement...")
                if not download_model(MODEL_URLS["GFPGANv1.4.pth"], models_dir / "GFPGANv1.4.pth"):
                    log_with_timestamp("GFPGAN download failed, continuing without enhancement")
            
            return True
        else:
            log_with_timestamp("Failed to download required models")
            log_with_timestamp("Please manually download models from:")
            for name, url in MODEL_URLS.items():
                log_with_timestamp(f"   {name}: {url}")
            return False

def list_available_models():
    """List all available models in the models directory with recommendations"""
    models_dir = ensure_models_directory()
    log_with_timestamp("📋 Available models:")
    
    # Check for face swapper models
    face_swapper_files = list(models_dir.glob("inswapper_*.onnx"))
    other_files = [f for f in models_dir.glob("*") if f.suffix in ['.onnx', '.pth'] and not f.name.startswith('inswapper_')]
    
    if not face_swapper_files and not other_files:
        log_with_timestamp("   No models found")
        log_with_timestamp("Download models from: https://github.com/Userfrom1995/FaceSwapLive/releases/tag/v1.0.0")
        return
    
    # List face swapper models with recommendations
    if face_swapper_files:
        log_with_timestamp("   Face Swapper Models:")
        for model_file in sorted(face_swapper_files):
            size_mb = model_file.stat().st_size / (1024 * 1024)
            if model_file.name == "inswapper_128.onnx":
                log_with_timestamp(f"   {model_file.name} ({size_mb:.1f} MB) - BEST QUALITY")
            elif model_file.name == "inswapper_128_fp16.onnx":
                log_with_timestamp(f"   {model_file.name} ({size_mb:.1f} MB) - FAST, LOWER VRAM")
            else:
                log_with_timestamp(f"   {model_file.name} ({size_mb:.1f} MB)")
    
    # List other models
    if other_files:
        log_with_timestamp("   Enhancement Models:")
        for model_file in sorted(other_files):
            size_mb = model_file.stat().st_size / (1024 * 1024)
            if model_file.name == "GFPGANv1.4.pth":
                log_with_timestamp(f"   {model_file.name} ({size_mb:.1f} MB) - FACE ENHANCEMENT")
            else:
                log_with_timestamp(f"   {model_file.name} ({size_mb:.1f} MB)")

def get_model_recommendations():
    """Provide model recommendations based on user's hardware/needs"""
    log_with_timestamp("Model Recommendations:")
    log_with_timestamp("   inswapper_128.onnx - Best quality, requires more VRAM")
    log_with_timestamp("   inswapper_128_fp16.onnx - Faster processing, less VRAM")
    log_with_timestamp("   GFPGANv1.4.pth - Face enhancement (optional but recommended)")
    log_with_timestamp("")
    log_with_timestamp("   Choose inswapper_128.onnx if you have 6GB+ VRAM")
    log_with_timestamp("   Choose inswapper_128_fp16.onnx if you have 4GB or less VRAM")