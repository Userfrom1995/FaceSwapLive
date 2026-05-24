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
from datetime import datetime
from typing import Optional, Tuple, Union
from config import config
from models import get_best_models

def log_info(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] INFO: {message}")

def log_error(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] ERROR: {message}")

class FaceSwapPipeline:
    """Face swap pipeline with minimal logging overhead"""
    
    def __init__(self):
        self.face_app = None
        self.face_swapper = None
        self.source_face = None
        
        # Performance tracking
        self.frame_counter = 0
        self.swap_counter = 0
        self.error_counter = 0
        self.processing_times = []
        self.max_time_samples = 20
    
    def initialize_models(self) -> bool:
        """Initialize models - only log critical errors"""
        try:
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
                log_info("GPU acceleration enabled")
            else:
                providers = ['CPUExecutionProvider']
                log_info("Using CPU processing")
            
            # Initialize face analysis
            self.face_app = FaceAnalysis(name='buffalo_l', providers=providers)
            self.face_app.prepare(ctx_id=0 if use_gpu else -1, det_size=(320, 320))
            
            # Ensure models are available (download if necessary)
            from models import ensure_models_available
            if not ensure_models_available():
                log_error("CRITICAL: Failed to ensure models are available!")
                return False
            
            # Get the best available face swapper model
            face_swapper_path, _ = get_best_models()
            
            if face_swapper_path and os.path.exists(face_swapper_path):
                try:
                    self.face_swapper = insightface.model_zoo.get_model(face_swapper_path, providers=providers)
                    
                    # Model warmup
                    dummy_img = np.random.randint(0, 255, (320, 320, 3), dtype=np.uint8)
                    self.face_app.get(dummy_img)
                    return True
                    
                except Exception as e:
                    log_error(f"Failed to load swapper: {e}")
                    return False
            else:
                log_error("CRITICAL: No face swapper model could be loaded!")
                return False
            
        except Exception as e:
            log_error(f"Model initialization error: {e}")
            return False
    
    def detect_face_optimized(self, image):
        """Optimized face detection"""
        try:
            faces = self.face_app.get(image)
            if faces:
                largest_face = max(faces, key=lambda x: (x.bbox[2] - x.bbox[0]) * (x.bbox[3] - x.bbox[1]))
                return largest_face
            return None
        except Exception as e:
            if self.error_counter % 100 == 0:
                log_error(f"Face detection error: {e}")
            return None
    
    def set_source_face(self, source_image) -> bool:
        """Set source face"""
        try:
            detected_face = self.detect_face_optimized(source_image)
            if detected_face is not None:
                self.source_face = detected_face
                print("Source face ready")
                return True
            else:
                self.source_face = None
                log_error("No face detected in source image")
                return False
        except Exception as e:
            log_error(f"Upload processing error: {e}")
            return False
    
    def process_frame_realtime(self, frame_data: Union[str, bytes]) -> Tuple[str, bool]:
        """ULTRA FAST frame processing with binary and OpenCV optimization"""
        self.frame_counter += 1
        if self.source_face is None or self.face_swapper is None:
            return frame_data if isinstance(frame_data, str) else "", False
        
        try:
            process_start = time.time()
            
            # Decode frame using OpenCV directly for max speed
            if isinstance(frame_data, str):
                if ',' in frame_data:
                    image_data = base64.b64decode(frame_data.split(',')[1])
                else:
                    image_data = base64.b64decode(frame_data)
            else:
                image_data = frame_data # Handle raw binary bytes
            
            nparr = np.frombuffer(image_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Face detection
            target_face = self.detect_face_optimized(frame)
            
            if target_face is not None:
                # Face swap using standard InsightFace API
                swapped_frame = self.face_swapper.get(frame, target_face, self.source_face, paste_back=True)
                self.swap_counter += 1
                
                # Convert and encode directly with OpenCV to JPEG
                quality = config.processing.JPEG_QUALITY
                _, buffer = cv2.imencode('.jpg', swapped_frame, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
                result_b64 = base64.b64encode(buffer).decode('utf-8')
                result_data = f"data:image/jpeg;base64,{result_b64}"
                
                # Timing tracking
                total_time = time.time() - process_start
                self.processing_times.append(total_time * 1000)
                if len(self.processing_times) > self.max_time_samples:
                    self.processing_times.pop(0)
                
                return result_data, True
            
            return frame_data if isinstance(frame_data, str) else "", False
        
        except Exception as e:
            self.error_counter += 1
            if self.error_counter % 50 == 0:
                log_error(f"Processing error #{self.error_counter}: {e}")
            return frame_data if isinstance(frame_data, str) else "", False
    
    def process_image(self, frame_data: str) -> Tuple[str, bool]:
        return self.process_frame_realtime(frame_data)
    
    def get_stats(self) -> dict:
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
        self.frame_counter = 0
        self.swap_counter = 0
        self.error_counter = 0
        self.processing_times = []
    
    def cleanup(self):
        self.source_face = None

_pipeline_instance = None

def get_pipeline() -> FaceSwapPipeline:
    global _pipeline_instance
    if _pipeline_instance is None:
        _pipeline_instance = FaceSwapPipeline()
    return _pipeline_instance

def initialize_pipeline() -> bool:
    pipeline = get_pipeline()
    return pipeline.initialize_models()
