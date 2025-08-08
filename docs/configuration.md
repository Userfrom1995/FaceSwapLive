# Configuration Reference

Complete reference for Face Swap Live configuration options.

## Configuration Hierarchy

Configuration is loaded in this order (highest priority first):

1. **Command Line Arguments** - Runtime parameters
2. **Environment Variables** - System-level settings  
3. **`.env` File** - Project defaults
4. **Built-in Defaults** - Default values in `config.py`

## Configuration Classes

### ServerConfig

Controls server behavior and network settings.

```python
class ServerConfig:
    HOST = '0.0.0.0'                    # Server bind address
    PORT_RANGE_START = 3000             # Port range start
    PORT_RANGE_END = 9999               # Port range end
    DEFAULT_PORT = 5000                 # Fallback port
    SECRET_KEY = 'faceswap_realtime_2025_secure_key'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB upload limit
    PING_TIMEOUT = 60                   # SocketIO ping timeout
    PING_INTERVAL = 25                  # SocketIO ping interval
    CORS_ALLOWED_ORIGINS = "*"          # CORS policy
    SINGLE_USER_MODE = True             # Single user enforcement
    DISCONNECT_PREVIOUS_USER = True     # Disconnect on new connection
```

**Environment Variables**:
- `FACESWAP_HOST`: Override HOST
- `FACESWAP_PORT`: Override DEFAULT_PORT

### ProcessingConfig

Controls face processing pipeline behavior.

```python
class ProcessingConfig:
    TARGET_FPS = 999                    # Maximum FPS target
    FRAME_SKIP_THRESHOLD = 0            # Frame skipping threshold
    MAX_PROCESSING_TIME = 50            # Max processing time (ms)
    WEBCAM_WIDTH = 640                  # Webcam resolution width
    WEBCAM_HEIGHT = 480                 # Webcam resolution height
    WEBCAM_FPS = 30                     # Webcam FPS
    JPEG_QUALITY = 85                   # Output JPEG quality
    CANVAS_ALPHA = False                # Alpha channel support
    IMAGE_SMOOTHING = True              # Image smoothing
    DETECTION_SIZE = (320, 320)         # Face detection size
    MIN_FACE_SIZE = 50                  # Minimum face size (pixels)
    CONFIDENCE_THRESHOLD = 0.5          # Detection confidence
```

**Environment Variables**:
- `FACESWAP_TARGET_FPS`: Override TARGET_FPS

### ModelConfig

Controls AI model management and paths.

```python
class ModelConfig:
    MODELS_DIR = Path("models")         # Models directory
    FACE_SWAPPER_MODELS = [             # Face swapper models
        "inswapper_128.onnx"
    ]
    ENHANCEMENT_MODELS = [              # Enhancement models
        "GFPGANv1.4.pth"
    ]
    MODEL_URLS = {                      # Download URLs
        "inswapper_128.onnx": "https://github.com/Userfrom1995/FaceSwapLive/releases/download/v1.0.0/inswapper_128.onnx",
        "GFPGANv1.4.pth": "https://github.com/Userfrom1995/FaceSwapLive/releases/download/v1.0.0/GFPGANv1.4.pth"
    }
    GPU_MEMORY_LIMIT = 12 * 1024 * 1024 * 1024  # GPU memory limit
    USE_GPU = True                      # GPU acceleration
    PROVIDERS_PRIORITY = [              # ONNX providers
        'CUDAExecutionProvider',
        'CPUExecutionProvider'
    ]
```

### NgrokConfig

Controls ngrok tunnel configuration.

```python
class NgrokConfig:
    ENABLE_NGROK = False                # Enable ngrok by default
    AUTH_TOKEN = None                   # Authentication token
    SUBDOMAIN = None                    # Custom subdomain
    REGION = "us"                       # Tunnel region
    DASHBOARD_PORT = 4040               # Dashboard port
    SHOW_TUNNEL_WARNING = True          # Security warnings
    AUTO_OPEN_BROWSER = True            # Auto-open browser
```

**Environment Variables**:
- `NGROK_AUTH_TOKEN`: Authentication token
- `NGROK_SUBDOMAIN`: Custom subdomain
- `NGROK_REGION`: Tunnel region
- `NGROK_DASHBOARD_PORT`: Dashboard port

### LoggingConfig

Controls logging and monitoring behavior.

```python
class LoggingConfig:
    ENABLE_CONSOLE_LOGGING = True       # Console output
    LOG_LEVEL = "INFO"                  # Logging level
    LOG_FORMAT = "[%(asctime)s] %(levelname)s: %(message)s"
    DATE_FORMAT = "%H:%M:%S"            # Time format
    ENABLE_PERFORMANCE_LOGGING = True   # Performance logs
    PERFORMANCE_LOG_INTERVAL = 30       # Log interval (frames)
    TRACK_PROCESSING_STATS = True       # Statistics tracking
    MAX_LOG_ENTRIES = 50                # Max log entries
```

### SecurityConfig

Controls security and validation settings.

```python
class SecurityConfig:
    ALLOWED_IMAGE_EXTENSIONS = {        # Allowed file types
        '.jpg', '.jpeg', '.png', '.bmp', '.webp'
    }
    MAX_IMAGE_SIZE = 10 * 1024 * 1024   # Max upload size
    MAX_FRAMES_PER_SECOND = 15          # Rate limiting
    SESSION_TIMEOUT = 300               # Session timeout (seconds)
    MAX_IDLE_TIME = 60                  # Idle timeout (seconds)
```

### DevelopmentConfig

Controls development and debugging features.

```python
class DevelopmentConfig:
    DEBUG_MODE = False                  # Flask debug mode
    ENABLE_RELOADER = False             # Auto-reload
    ENABLE_CORS = True                  # CORS support
    VERBOSE_LOGGING = False             # Verbose logs
    SAVE_DEBUG_IMAGES = False           # Save debug images
```

## Command Line Arguments

### Basic Arguments

```bash
python app.py [OPTIONS]
```

**Options**:
- `--host HOST`: Server host address (default: 0.0.0.0)
- `--port PORT`: Server port number (default: auto-detect)
- `--debug`: Enable debug mode
- `--no-gpu`: Disable GPU acceleration
- `--models-dir PATH`: Models directory path

### Ngrok Arguments

- `--ngrok`: Enable ngrok tunnel
- `--ngrok-auth-token TOKEN`: Authentication token
- `--ngrok-subdomain NAME`: Custom subdomain (paid plan)
- `--ngrok-region REGION`: Tunnel region

### Examples

```bash
# Basic local server
python app.py

# Specific port
python app.py --port 8080

# Debug mode
python app.py --debug

# Ngrok tunnel
python app.py --ngrok --ngrok-auth-token abc123

# Custom subdomain
python app.py --ngrok --ngrok-subdomain demo --ngrok-region eu

# Disable GPU
python app.py --no-gpu

# Custom models directory
python app.py --models-dir /path/to/models
```

## Environment Variables

### Server Configuration

```bash
export FACESWAP_HOST=127.0.0.1
export FACESWAP_PORT=8080
```

### Processing Configuration

```bash
export FACESWAP_TARGET_FPS=30
export FACESWAP_DISABLE_GPU=true
```

### Ngrok Configuration

```bash
export NGROK_AUTH_TOKEN=your_token_here
export NGROK_SUBDOMAIN=your-subdomain
export NGROK_REGION=eu
export NGROK_DASHBOARD_PORT=4041
```

## Configuration Files

### .env File

Create a `.env` file in the project root:

```bash
# Server Configuration
FACESWAP_HOST=0.0.0.0
FACESWAP_PORT=5000

# Ngrok Configuration
NGROK_AUTH_TOKEN=your_token_here
NGROK_SUBDOMAIN=faceswap-demo
NGROK_REGION=us

# Processing Configuration
FACESWAP_TARGET_FPS=30
```

### Configuration Loading

The configuration system loads settings in this order:

1. **Default Values**: From `config.py` classes
2. **Environment Variables**: Override defaults
3. **Command Line**: Override environment variables

## Performance Tuning

### High Performance Configuration

For maximum performance:

```python
# Processing optimizations
TARGET_FPS = 999
FRAME_SKIP_THRESHOLD = 0
MAX_PROCESSING_TIME = 30
JPEG_QUALITY = 75

# GPU optimizations
GPU_MEMORY_LIMIT = 8 * 1024 * 1024 * 1024  # 8GB
USE_GPU = True

# Server optimizations
PING_TIMEOUT = 30
PING_INTERVAL = 10
```

### Low Resource Configuration

For limited resources:

```python
# Reduced quality for performance
TARGET_FPS = 15
JPEG_QUALITY = 70
WEBCAM_WIDTH = 480
WEBCAM_HEIGHT = 360

# Conservative memory usage
GPU_MEMORY_LIMIT = 2 * 1024 * 1024 * 1024  # 2GB
FRAME_SKIP_THRESHOLD = 2
```

## Security Configuration

### Production Security

For production deployment:

```python
# Strict security
CORS_ALLOWED_ORIGINS = "https://yourdomain.com"
MAX_FRAMES_PER_SECOND = 10
SESSION_TIMEOUT = 180
MAX_IDLE_TIME = 30

# File upload restrictions
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png'}
```

### Development Security

For development:

```python
# Relaxed for development
CORS_ALLOWED_ORIGINS = "*"
MAX_FRAMES_PER_SECOND = 30
SESSION_TIMEOUT = 600
DEBUG_MODE = True
VERBOSE_LOGGING = True
```

## Monitoring Configuration

### Performance Monitoring

```python
# Detailed monitoring
ENABLE_PERFORMANCE_LOGGING = True
PERFORMANCE_LOG_INTERVAL = 10
TRACK_PROCESSING_STATS = True
MAX_LOG_ENTRIES = 100
```

### Production Monitoring

```python
# Production logging
LOG_LEVEL = "WARNING"
ENABLE_PERFORMANCE_LOGGING = False
VERBOSE_LOGGING = False
SAVE_DEBUG_IMAGES = False
```

## Troubleshooting Configuration

### Debug Configuration

For troubleshooting:

```bash
python app.py --debug --verbose
```

```python
# Debug settings
DEBUG_MODE = True
VERBOSE_LOGGING = True
SAVE_DEBUG_IMAGES = True
LOG_LEVEL = "DEBUG"
```

### Common Issues

**High Memory Usage**:
```python
GPU_MEMORY_LIMIT = 4 * 1024 * 1024 * 1024  # Reduce to 4GB
FRAME_SKIP_THRESHOLD = 1  # Skip frames
```

**Low Performance**:
```python
TARGET_FPS = 15  # Reduce target FPS
JPEG_QUALITY = 70  # Reduce quality
MAX_PROCESSING_TIME = 100  # Increase timeout
```

**Connection Issues**:
```python
PING_TIMEOUT = 120  # Increase timeout
PING_INTERVAL = 30  # Reduce frequency
```

## Configuration Validation

The system validates configuration on startup:

- **Port Ranges**: Ensures valid port numbers
- **File Paths**: Validates directory existence
- **Memory Limits**: Checks against system limits
- **Model URLs**: Validates URL format
- **Token Format**: Validates ngrok token format

## Advanced Configuration

### Custom Providers

```python
# Custom ONNX providers
PROVIDERS_PRIORITY = [
    ('TensorrtExecutionProvider', {
        'device_id': 0,
        'trt_max_workspace_size': 2147483648,
    }),
    'CUDAExecutionProvider',
    'CPUExecutionProvider'
]
```

### Model Customization

```python
# Custom model configuration
FACE_SWAPPER_MODELS = ["custom_model.onnx"]
MODEL_URLS = {
    "custom_model.onnx": "https://your-server.com/model.onnx"
}
```

### Network Customization

```python
# Custom network settings
HOST = '192.168.1.100'  # Specific interface
PORT_RANGE_START = 8000
PORT_RANGE_END = 8999
CORS_ALLOWED_ORIGINS = ["https://app1.com", "https://app2.com"]
```