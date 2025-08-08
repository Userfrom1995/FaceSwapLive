#!/usr/bin/env python3
"""
Test script to verify GPU/CPU fallback functionality
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_gpu_configuration():
    """Test GPU configuration and fallback mechanisms"""
    print("Testing GPU Configuration and Fallback")
    print("=" * 50)
    
    # Test 1: Check torch CUDA availability
    print("\n1. Testing PyTorch CUDA availability:")
    try:
        import torch
        cuda_available = torch.cuda.is_available()
        print(f"   PyTorch CUDA available: {cuda_available}")
        if cuda_available:
            print(f"   GPU device: {torch.cuda.get_device_name(0)}")
            print(f"   GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    except ImportError:
        print("   PyTorch not installed")
        cuda_available = False
    
    # Test 2: Check default configuration
    print("\n2. Testing default configuration:")
    try:
        from config import config
        print(f"   config.models.USE_GPU: {config.models.USE_GPU}")
        print(f"   GPU_MEMORY_LIMIT: {config.models.GPU_MEMORY_LIMIT / 1024**3:.1f} GB")
        print(f"   PROVIDERS_PRIORITY: {config.models.PROVIDERS_PRIORITY}")
    except Exception as e:
        print(f"   Error loading config: {e}")
        return False
    
    # Test 3: Test --no-gpu flag simulation
    print("\n3. Testing --no-gpu flag simulation:")
    try:
        # Simulate --no-gpu flag
        original_use_gpu = config.models.USE_GPU
        config.models.USE_GPU = False
        print(f"   After --no-gpu: config.models.USE_GPU = {config.models.USE_GPU}")
        
        # Test pipeline provider selection
        use_gpu = config.models.USE_GPU and cuda_available
        print(f"   Effective GPU usage: {use_gpu}")
        
        if use_gpu:
            providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
            ctx_id = 0
        else:
            providers = ['CPUExecutionProvider']
            ctx_id = -1
        
        print(f"   Selected providers: {providers}")
        print(f"   InsightFace ctx_id: {ctx_id}")
        
        # Restore original setting
        config.models.USE_GPU = original_use_gpu
        
    except Exception as e:
        print(f"   Error testing --no-gpu: {e}")
    
    # Test 4: Test environment variable
    print("\n4. Testing FACESWAP_DISABLE_GPU environment variable:")
    try:
        import os
        
        # Set environment variable
        os.environ['FACESWAP_DISABLE_GPU'] = 'true'
        
        # Reload config
        from config import load_environment_overrides
        load_environment_overrides()
        
        print(f"   After env var: config.models.USE_GPU = {config.models.USE_GPU}")
        
        # Clean up
        del os.environ['FACESWAP_DISABLE_GPU']
        config.models.USE_GPU = True  # Reset to default
        
    except Exception as e:
        print(f"   Error testing env var: {e}")
    
    # Test 5: Test pipeline initialization
    print("\n5. Testing pipeline initialization:")
    try:
        from pipeline import FaceSwapPipeline
        
        # Test with GPU enabled
        config.models.USE_GPU = True
        pipeline_gpu = FaceSwapPipeline()
        print("   GPU pipeline created successfully")
        
        # Test with GPU disabled
        config.models.USE_GPU = False
        pipeline_cpu = FaceSwapPipeline()
        print("   CPU pipeline created successfully")
        
        # Reset to default
        config.models.USE_GPU = True
        
    except Exception as e:
        print(f"   Error testing pipeline: {e}")
    
    print("\n" + "=" * 50)
    print("GPU configuration test completed!")
    
    return True

def test_cpu_only_mode():
    """Test CPU-only mode functionality"""
    print("\nTesting CPU-Only Mode")
    print("=" * 30)
    
    try:
        from config import config
        from pipeline import FaceSwapPipeline
        
        # Force CPU mode
        original_use_gpu = config.models.USE_GPU
        config.models.USE_GPU = False
        
        print("Initializing pipeline in CPU-only mode...")
        pipeline = FaceSwapPipeline()
        
        # This would normally initialize models, but we'll just test the setup
        print("CPU-only pipeline created successfully")
        print("Note: Full model initialization requires actual model files")
        
        # Restore original setting
        config.models.USE_GPU = original_use_gpu
        
        return True
        
    except Exception as e:
        print(f"Error in CPU-only test: {e}")
        return False

if __name__ == "__main__":
    success = test_gpu_configuration()
    if success:
        test_cpu_only_mode()