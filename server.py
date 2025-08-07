"""
Face Swap Live - Server Implementation
OPTIMIZED for maximum performance - minimal logging overhead
"""

from flask import Flask, render_template, request, Response, jsonify
from flask_socketio import SocketIO, emit, disconnect
import socket
import random
import time
import threading
import logging
from datetime import datetime
from config import config
from pipeline import get_pipeline, initialize_pipeline

# Disable Flask/SocketIO logging for performance
logging.getLogger('werkzeug').disabled = True
logging.getLogger('socketio').disabled = True
logging.getLogger('engineio').disabled = True

def log_with_timestamp(message):
    """DISABLED for performance - only critical errors"""
    pass

def log_error(message):
    """Log only critical errors"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] ERROR: {message}")

def log_info(message):
    """Log only important info"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

class OptimizedFaceSwapServer:
    """Ultra-fast server with minimal overhead"""
    
    def __init__(self):
        self.app = None
        self.socketio = None
        self.pipeline = get_pipeline()
        
        # Minimal session tracking
        self.current_user = None
        self.processing_active = False
        
        # Performance counters (minimal)
        self.total_frames = 0
        self.successful_swaps = 0
    
    def find_available_port(self):
        """Quickly find available port"""
        for _ in range(20):
            port = random.randint(3000, 9000)
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.1)
                result = sock.connect_ex(('localhost', port))
                sock.close()
                if result != 0:
                    return port
            except:
                continue
        return 5000
    
    def create_app(self):
        """Create minimal Flask app"""
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'faceswap_optimized'
        app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
        return app
    
    def setup_routes(self):
        """Setup minimal routes"""
        @self.app.route('/')
        def index():
            return render_template('index.html')
        
        @self.app.route('/upload_source', methods=['POST'])
        def upload_source():
            try:
                if 'image' not in request.files:
                    return jsonify({'success': False, 'message': 'No image'})
                
                file = request.files['image']
                if file.filename == '':
                    return jsonify({'success': False, 'message': 'No file'})
                
                # Fast processing
                image_data = file.read()
                from PIL import Image
                import cv2
                import numpy as np
                import io
                
                image = Image.open(io.BytesIO(image_data))
                frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                
                if self.pipeline.set_source_face(frame):
                    return jsonify({'success': True, 'message': 'Source face ready!'})
                else:
                    return jsonify({'success': False, 'message': 'No face detected'})
            except Exception as e:
                log_error(f"Upload error: {e}")
                return jsonify({'success': False, 'message': f'Error: {str(e)}'})
        
        @self.app.route('/status')
        def get_status():
            return jsonify(self.pipeline.get_stats())
    
    def setup_socketio(self):
        """Fast SocketIO setup"""
        @self.socketio.on('connect')
        def handle_connect():
            if config.server.SINGLE_USER_MODE and self.current_user:
                if self.current_user != request.sid:
                    disconnect()
                    return
            self.current_user = request.sid
            self.processing_active = True
            # Removed verbose logging
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            if request.sid == self.current_user:
                self.current_user = None
                self.processing_active = False
        
        @self.socketio.on('process_frame')
        def handle_frame_processing(data):
            """ULTRA FAST frame processing - no logging overhead"""
            if request.sid != self.current_user or not self.processing_active:
                return
            
            self.total_frames += 1
            
            try:
                # Use optimized pipeline method - NO LOGGING
                frame_data = data.get('frame', '')
                processed_data, success = self.pipeline.process_frame_realtime(frame_data)
                
                if success:
                    self.successful_swaps += 1
                
                # Minimal response - only send essential data
                response = {
                    'success': success,
                    'processed': processed_data
                }
                
                # Only send stats every 30th frame to reduce overhead
                if self.total_frames % 30 == 0:
                    stats = self.pipeline.get_stats()
                    response['stats'] = {
                        'frame_count': stats['frame_count'],
                        'swap_count': stats['swap_count'],
                        'avg_processing_time': stats['avg_processing_time'],
                        'fps': round(self.total_frames / max(1, time.time() - getattr(self, 'start_time', time.time())), 1)
                    }
                
                emit('processed_frame', response)
                
            except Exception as e:
                # Silent error handling for speed
                emit('processed_frame', {
                    'success': False,
                    'error': str(e),
                    'processed': data.get('frame', '')
                })
        
        @self.socketio.on('clear_source')
        def handle_clear_source():
            if request.sid == self.current_user:
                self.pipeline.source_face = None
                emit('status_update', {'message': 'Source cleared'})
    
    def start_server(self, host='0.0.0.0', port=None):
        """Start optimized server"""
        try:
            if port is None:
                port = self.find_available_port()
            
            # Create app and socketio
            self.app = self.create_app()
            self.socketio = SocketIO(
                self.app,
                cors_allowed_origins="*",
                async_mode='threading',
                logger=False,
                engineio_logger=False,
                ping_timeout=30,
                ping_interval=10
            )
            
            # Setup routes and events
            self.setup_routes()
            self.setup_socketio()
            
            # Track start time for FPS calculation
            self.start_time = time.time()
            
            # Minimal startup info
            log_info("=" * 50)
            log_info("⚡ OPTIMIZED FACE SWAP SERVER")
            log_info(f"🌐 URL: http://{host}:{port}")
            log_info("🚀 Performance Mode: MAXIMUM")
            log_info("🛑 Press Ctrl+C to stop")
            log_info("=" * 50)
            
            self.socketio.run(
                self.app,
                host=host,
                port=port,
                debug=False,
                allow_unsafe_werkzeug=True,
                log_output=False
            )
            return True
            
        except KeyboardInterrupt:
            log_info("Server stopped by user")
        except Exception as e:
            log_error(f"Server error: {e}")
        finally:
            log_info("Cleanup complete")

# Global server instance
_server_instance = None

def create_server():
    """Create server instance"""
    global _server_instance
    _server_instance = OptimizedFaceSwapServer()
    return _server_instance

def start_server(host='0.0.0.0', port=None):
    """Start the optimized server"""
    server = create_server()
    return server.start_server(host, port)

if __name__ == "__main__":
    start_server()