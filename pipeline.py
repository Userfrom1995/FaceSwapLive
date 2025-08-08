"""
Face Swap Live - Processing Pipeline
OPTIMIZED for maximum performance - minimal logging overhead
"""
import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
import torch
import base64
import io
from PIL import Image
import time
import os
import traceback
from datetime import datetime
from typing import Optional, Tuple, Union
from config import config
from models import get_best_models

def log_with_timestamp(message):
    """ONLY log critical errors - removed performance overhead"""
    pass  # Disabled for performance

def log_error(message):
    """Log only critical errors"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] ERROR: {message}")

class FaceSwapPipeline:
    """Face swap pipeline with minimal logging overhead"""
    
    def __init__(self):
        self.face_app = None
        self.face_swapper = None
        self.source_face = None
        
        # Performance tracking (minimal)
        self.frame_counter = 0
        self.swap_counter = 0
        self.error_counter = 0
        self.processing_times = []
        self.max_time_samples = 20  # Reduced from 100
        
        # Remove verbose logging
        # log_with_timestamp("Face swap pipeline created")
    
    def initialize_models(self) -> bool:
        """Initialize models - only log critical errors"""
        try:
            # log_with_timestamp("⚡ Initializing face processing models...")
            
            # GPU optimization - respect configuration
            from config import config
            use_gpu = config.models.USE_GPU and torch.cuda.is_available()
            
            if use_gpu:
                providers = [
                    ('CUDAExecutionProvider', {
                        'device_id': 0,
                        'gpu_mem_limit': config.models.GPU_MEMORY_LIMIT,
                        'arena_extend_strategy': 'kNextPowerOfTwo',
                        'cudnn_conv_algo_search': 'HEURISTIC',
                        'do_copy_in_default_stream': True,
                    }),
                    'CPUExecutionProvider'
                ]
                log_error("GPU acceleration enabled")
            else:
                providers = ['CPUExecutionProvider']
                if not torch.cuda.is_available():
                    log_error("CUDA not available, using CPU processing")
                else:
                    log_error("GPU disabled by configuration, using CPU processing")
            
            # Initialize face analysis
            # log_with_timestamp("🔄 Loading face analysis model...")
            self.face_app = FaceAnalysis(name='buffalo_l', providers=providers)
            self.face_app.prepare(ctx_id=0 if use_gpu else -1, det_size=(320, 320))
            # log_with_timestamp("✅ Face analysis model ready")
            
            # Ensure models are available (download if necessary)
            from models import ensure_models_available
            if not ensure_models_available():
                log_error("CRITICAL: Failed to ensure models are available!")
                return False
            
            # Get the best available face swapper model
            face_swapper_path, _ = get_best_models()
            
            if face_swapper_path and os.path.exists(face_swapper_path):
                try:
                    # log_with_timestamp(f"🔄 Loading: {face_swapper_path}")
                    self.face_swapper = insightface.model_zoo.get_model(face_swapper_path, providers=providers)
                    # log_with_timestamp(f"✅ Face swapper loaded: {os.path.basename(face_swapper_path)}")
                    
                    # Model warmup - silent
                    dummy_img = np.random.randint(0, 255, (320, 320, 3), dtype=np.uint8)
                    self.face_app.get(dummy_img)
                    # log_with_timestamp("🔥 Model warmup completed")
                    return True
                    
                except Exception as e:
                    log_error(f"Failed to load {face_swapper_path}: {e}")
                    return False
            else:
                log_error("CRITICAL: No face swapper model could be loaded!")
                return False
            
        except Exception as e:
            log_error(f"Model initialization error: {e}")
            return False
    
    def detect_face_optimized(self, image):
        """Optimized face detection - no logging for performance"""
        try:
            # log_with_timestamp(f"🔍 Analyzing image shape: {image.shape}")
            faces = self.face_app.get(image)
            
            if faces:
                # log_with_timestamp(f"👥 Detected {len(faces)} face(s)")
                # Return largest face
                largest_face = max(faces, key=lambda x: (x.bbox[2] - x.bbox[0]) * (x.bbox[3] - x.bbox[1]))
                # bbox = largest_face.bbox
                # log_with_timestamp(f"📐 Best face bbox: [{bbox[0]:.1f}, {bbox[1]:.1f}, {bbox[2]:.1f}, {bbox[3]:.1f}]")
                return largest_face
            else:
                # log_with_timestamp("❌ No faces detected in frame")
                return None
                
        except Exception as e:
            # Only log every 100th error to avoid spam
            if self.error_counter % 100 == 0:
                log_error(f"Face detection error: {e}")
            return None
    
    def set_source_face(self, source_image) -> bool:
        """Set source face - minimal logging"""
        try:
            detected_face = self.detect_face_optimized(source_image)
            
            if detected_face is not None:
                self.source_face = detected_face
                # log_with_timestamp("✅ Source face extracted and stored successfully!")
                print("Source face ready")  # Only success message
                return True
            else:
                self.source_face = None
                log_error("No face detected in source image")
                return False
                
        except Exception as e:
            log_error(f"Upload processing error: {e}")
            return False
    
    def process_frame_realtime(self, frame_data: str) -> Tuple[str, bool]:
        """
        ULTRA FAST frame processing - removed all logging overhead
        """
        self.frame_counter += 1
        
        # Skip ALL logging for performance - only track counts
        if self.source_face is None or self.face_swapper is None:
            return frame_data, False
        
        try:
            process_start = time.time()
            
            # Decode frame - NO LOGGING
            if ',' in frame_data:
                image_data = base64.b64decode(frame_data.split(',')[1])
            else:
                image_data = base64.b64decode(frame_data)
            
            image = Image.open(io.BytesIO(image_data))
            frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Face detection - NO LOGGING
            target_face = self.detect_face_optimized(frame)
            
            if target_face is not None:
                # Face swap - NO LOGGING
                swapped_frame = self.face_swapper.get(frame, target_face, self.source_face, paste_back=True)
                self.swap_counter += 1
                
                # Quick enhancement
                enhanced_frame = cv2.convertScaleAbs(swapped_frame, alpha=1.05, beta=5)
                
                # Convert and encode - NO LOGGING
                result_rgb = cv2.cvtColor(enhanced_frame, cv2.COLOR_BGR2RGB)
                result_image = Image.fromarray(result_rgb)
                
                buffer = io.BytesIO()
                result_image.save(buffer, format='JPEG', quality=85)
                result_b64 = base64.b64encode(buffer.getvalue()).decode()
                result_data = f"data:image/jpeg;base64,{result_b64}"
                
                # Minimal timing tracking
                total_time = time.time() - process_start
                self.processing_times.append(total_time * 1000)
                if len(self.processing_times) > self.max_time_samples:
                    self.processing_times.pop(0)
                
                return result_data, True
            
            else:
                # No logging for missing faces - too frequent
                return frame_data, False
        
        except Exception as e:
            self.error_counter += 1
            # Only log every 50th error to avoid spam
            if self.error_counter % 50 == 0:
                log_error(f"Processing error #{self.error_counter}: {e}")
            return frame_data, False
    
    def process_image(self, frame_data: str) -> Tuple[str, bool]:
        """Process single image - delegates to realtime method"""
        result_data, success = self.process_frame_realtime(frame_data)
        return result_data, success
    
    def get_stats(self) -> dict:
        """Get performance statistics"""
        avg_time = sum(self.processing_times) / len(self.processing_times) if self.processing_times else 0
        
        return {
            'frame_count': self.frame_counter,
            'swap_count': self.swap_counter,
            'error_count': self.error_counter,
            'avg_processing_time': round(avg_time, 2),
            'processing_time': round(self.processing_times[-1], 2) if self.processing_times else 0,
            'source_face_loaded': self.source_face is not None,
            'models_loaded': self.face_swapper is not None
        }
    
    def reset_stats(self):
        """Reset performance counters"""
        self.frame_counter = 0
        self.swap_counter = 0
        self.error_counter = 0
        self.processing_times = []
    
    def cleanup(self):
        """Cleanup resources"""
        self.source_face = None

# Global pipeline instance
_pipeline_instance = None

def get_pipeline() -> FaceSwapPipeline:
    """Get the global pipeline instance"""
    global _pipeline_instance
    if _pipeline_instance is None:
        _pipeline_instance = FaceSwapPipeline()
    return _pipeline_instance

def initialize_pipeline() -> bool:
    """Initialize the global pipeline"""
    pipeline = get_pipeline()
    return pipeline.initialize_models()