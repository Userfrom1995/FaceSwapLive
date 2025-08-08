#!/usr/bin/env python3
"""
Debug script to show exactly what's happening with model loading
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def debug_pipeline_init():
    """Debug the pipeline initialization process"""
    print("🔍 DEBUGGING PIPELINE INITIALIZATION")
    print("=" * 60)
    
    # Step 1: Check models directory
    from config import config
    models_dir = config.models.MODELS_DIR
    print(f"\n1. Models directory: {models_dir}")
    print(f"   Exists: {models_dir.exists()}")
    if models_dir.exists():
        model_files = list(models_dir.glob("*"))
        print(f"   Files: {[f.name for f in model_files]}")
    
    # Step 2: Test get_best_models
    print(f"\n2. Testing get_best_models():")
    try:
        from models import get_best_models
        face_swapper_path, face_analysis_path = get_best_models()
        print(f"   Face swapper path: {face_swapper_path}")
        print(f"   Face analysis path: {face_analysis_path}")
        print(f"   Face swapper exists: {face_swapper_path and Path(face_swapper_path).exists() if face_swapper_path else False}")
    except Exception as e:
        print(f"   ERROR: {e}")
    
    # Step 3: Test ensure_models_available
    print(f"\n3. Testing ensure_models_available():")
    try:
        from models import ensure_models_available
        result = ensure_models_available()
        print(f"   Result: {result}")
    except Exception as e:
        print(f"   ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    # Step 4: Test pipeline initialization
    print(f"\n4. Testing pipeline initialization:")
    try:
        from pipeline import initialize_pipeline
        result = initialize_pipeline()
        print(f"   Result: {result}")
    except Exception as e:
        print(f"   ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("🎯 Debug completed!")

if __name__ == "__main__":
    debug_pipeline_init()