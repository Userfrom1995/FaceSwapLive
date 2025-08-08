#!/usr/bin/env python3
"""
Test script to verify model download functionality
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from models import ensure_models_available, get_best_models, list_available_models

def test_model_system():
    """Test the model download and detection system"""
    print("🧪 Testing Face Swap Live Model System")
    print("=" * 50)
    
    # Test 1: List current models
    print("\n1. Current models in directory:")
    list_available_models()
    
    # Test 2: Get best models (before download)
    print("\n2. Best available models (before download):")
    face_swapper_path, face_analysis_path = get_best_models()
    print(f"   Face Swapper: {face_swapper_path}")
    print(f"   Face Analysis: {face_analysis_path}")
    
    # Test 3: Ensure models are available (this should trigger download)
    print("\n3. Ensuring models are available (may download):")
    success = ensure_models_available()
    print(f"   Result: {'✅ SUCCESS' if success else '❌ FAILED'}")
    
    # Test 4: Get best models (after download)
    print("\n4. Best available models (after download):")
    face_swapper_path, face_analysis_path = get_best_models()
    print(f"   Face Swapper: {face_swapper_path}")
    print(f"   Face Analysis: {face_analysis_path}")
    
    # Test 5: List models again
    print("\n5. Models after download attempt:")
    list_available_models()
    
    print("\n" + "=" * 50)
    print("🎯 Test completed!")
    
    return success

if __name__ == "__main__":
    test_model_system()