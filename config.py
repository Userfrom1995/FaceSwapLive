"""
Face Swap Live - Configuration Settings

This module contains all configuration parameters for the Face Swap Live application.
Modify these settings to customize server behavior, performance, and processing parameters.
"""

import os
from pathlib import Path

# =============================================================================
# SERVER CONFIGURATION
# =============================================================================

class ServerConfig:
    """Server-related configuration parameters"""
    
    # Network settings
    HOST = '0.0.0.0'  # Listen on all interfaces (use '127.0.0.1' for localhost only)
    PORT_RANGE_START = 3000  # Starting port for random selection
    PORT_RANGE_END = 9999    # Ending port for random selection
    DEFAULT_PORT = 5000      # Fallback port if random selection fails
    
    # Flask settings
    SECRET_KEY = 'faceswap_realtime_2025_secure_key'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file upload size
    
    # SocketIO settings
    PING_TIMEOUT = 60        # Client ping timeout in seconds
    PING_INTERVAL = 25       # Ping interval in seconds
    CORS_ALLOWED_ORIGINS = "*"  # CORS policy (use specific domains in production)
    
    # Single user enforcement
    SINGLE_USER_MODE = True  # Only allow one user at a time
    DISCONNECT_PREVIOUS_USER = True  # Disconnect previous user when new one connects

# =============================================================================
# PROCESSING CONFIGURATION
# =============================================================================

class ProcessingConfig:
    """Face processing and pipeline configuration"""
    
    # Performance settings - MAXIMUM FPS by default
    TARGET_FPS = 999         # Maximum possible FPS (let pipeline decide optimal rate)
    FRAME_SKIP_THRESHOLD = 0 # No frame skipping for maximum performance
    MAX_PROCESSING_TIME = 50   # Maximum processing time per frame (ms)
    
    # Image processing settings
    WEBCAM_WIDTH = 640       # Preferred webcam width
    WEBCAM_HEIGHT = 480      # Preferred webcam height
    WEBCAM_FPS = 30          # Preferred webcam FPS
    
    # Quality settings
    JPEG_QUALITY = 85        # JPEG compression quality (1-100)
    CANVAS_ALPHA = False     # Disable alpha channel for better performance
    IMAGE_SMOOTHING = True   # Enable image smoothing
    
    # Face detection settings
    DETECTION_SIZE = (320, 320)  # Face detection input size
    MIN_FACE_SIZE = 50       # Minimum face size in pixels
    CONFIDENCE_THRESHOLD = 0.5  # Face detection confidence threshold

# =============================================================================
# MODEL CONFIGURATION
# =============================================================================

class ModelConfig:
    """AI model configuration and paths"""
    
    # Model directory
    MODELS_DIR = Path(__file__).parent / "models"
    
    # Face swapper model (best quality only)
    FACE_SWAPPER_MODELS = [
        "inswapper_128.onnx",           # High quality model
    ]
    
    # Face enhancement models
    ENHANCEMENT_MODELS = [
        "GFPGANv1.4.pth",              # GFPGAN enhancement model
    ]
    
    # Model download URLs
    MODEL_URLS = {
        "inswapper_128.onnx": "https://github.com/Userfrom1995/FaceSwapLive/releases/download/v1.0.0/inswapper_128.onnx",
        "GFPGANv1.4.pth": "https://github.com/Userfrom1995/FaceSwapLive/releases/download/v1.0.0/GFPGANv1.4.pth"
    }
    
    # Alternative download sources (if needed)
    ALTERNATIVE_URLS = {
        # Add alternative sources here if main URLs fail
    }
    
    # GPU settings
    GPU_MEMORY_LIMIT = 12 * 1024 * 1024 * 1024  # 12GB GPU memory limit
    USE_GPU = True           # Enable GPU acceleration if available
    PROVIDERS_PRIORITY = [   # ONNX Runtime providers in priority order
        'CUDAExecutionProvider',
        'CPUExecutionProvider'
    ]

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

class LoggingConfig:
    """Logging and monitoring configuration"""
    
    # Console logging
    ENABLE_CONSOLE_LOGGING = True
    LOG_LEVEL = "INFO"       # DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_FORMAT = "[%(asctime)s] %(levelname)s: %(message)s"
    DATE_FORMAT = "%H:%M:%S"
    
    # Performance monitoring
    ENABLE_PERFORMANCE_LOGGING = True
    PERFORMANCE_LOG_INTERVAL = 30  # Log performance every N frames
    
    # Statistics tracking
    TRACK_PROCESSING_STATS = True
    MAX_LOG_ENTRIES = 50     # Maximum log entries to keep in memory

# =============================================================================
# SECURITY CONFIGURATION
# =============================================================================

class SecurityConfig:
    """Security and validation settings"""
    
    # File upload validation
    ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}
    MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB maximum image size
    
    # Rate limiting (frames per second per user)
    MAX_FRAMES_PER_SECOND = 15
    
    # Session management
    SESSION_TIMEOUT = 300    # Session timeout in seconds (5 minutes)
    MAX_IDLE_TIME = 60       # Maximum idle time before cleanup (seconds)

# =============================================================================
# DEVELOPMENT CONFIGURATION
# =============================================================================

class DevelopmentConfig:
    """Development and debugging settings"""
    
    # Debug settings
    DEBUG_MODE = False       # Enable Flask debug mode
    ENABLE_RELOADER = False  # Enable auto-reload on code changes
    
    # Development features
    ENABLE_CORS = True       # Enable CORS for development
    VERBOSE_LOGGING = False  # Enable verbose logging
    SAVE_DEBUG_IMAGES = False  # Save processed images for debugging


class NgrokConfig:
    """Ngrok tunnel configuration"""
    
    # Ngrok settings
    ENABLE_NGROK = False     # Enable ngrok tunnel by default
    AUTH_TOKEN = None        # Ngrok auth token (set via environment or command line)
    SUBDOMAIN = None         # Custom subdomain (requires paid plan)
    REGION = "us"           # Ngrok region: us, eu, ap, au, sa, jp, in
    DASHBOARD_PORT = 4040    # Ngrok dashboard port (default: 4040)
    
    # Security settings
    SHOW_TUNNEL_WARNING = True  # Show security warning when tunnel is active
    AUTO_OPEN_BROWSER = True    # Automatically open browser with tunnel URL

# =============================================================================
# CONFIGURATION FACTORY
# =============================================================================

def get_config():
    """
    Get the appropriate configuration based on environment.
    Returns a configuration object with all settings.
    """
    
    class Config:
        """Combined configuration class"""
        def __init__(self):
            self.server = ServerConfig()
            self.processing = ProcessingConfig()
            self.models = ModelConfig()
            self.logging = LoggingConfig()
            self.security = SecurityConfig()
            self.development = DevelopmentConfig()
            self.ngrok = NgrokConfig()
            
            # Ensure models directory exists
            self.models.MODELS_DIR.mkdir(exist_ok=True)
    
    return Config()

# Create default configuration instance
config = get_config()

# =============================================================================
# ENVIRONMENT OVERRIDES
# =============================================================================

def load_environment_overrides():
    """
    Load configuration overrides from environment variables.
    This allows customization without modifying the code.
    """
    
    # Server overrides
    if os.getenv('FACESWAP_HOST'):
        config.server.HOST = os.getenv('FACESWAP_HOST')
    
    if os.getenv('FACESWAP_PORT'):
        try:
            config.server.DEFAULT_PORT = int(os.getenv('FACESWAP_PORT'))
        except ValueError:
            pass
    
    # Processing overrides
    if os.getenv('FACESWAP_TARGET_FPS'):
        try:
            config.processing.TARGET_FPS = int(os.getenv('FACESWAP_TARGET_FPS'))
        except ValueError:
            pass
    
    # GPU override
    if os.getenv('FACESWAP_DISABLE_GPU'):
        config.models.USE_GPU = False
    
    # Ngrok overrides
    if os.getenv('NGROK_AUTH_TOKEN'):
        config.ngrok.AUTH_TOKEN = os.getenv('NGROK_AUTH_TOKEN')
    
    if os.getenv('NGROK_SUBDOMAIN'):
        config.ngrok.SUBDOMAIN = os.getenv('NGROK_SUBDOMAIN')
    
    if os.getenv('NGROK_REGION'):
        config.ngrok.REGION = os.getenv('NGROK_REGION')
    
    if os.getenv('NGROK_DASHBOARD_PORT'):
        try:
            config.ngrok.DASHBOARD_PORT = int(os.getenv('NGROK_DASHBOARD_PORT'))
        except ValueError:
            pass

# Load environment overrides on import
load_environment_overrides()