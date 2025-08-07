# Face Swap Live - Real-time Face Swapping Server

A high-performance, real-time face swapping application optimized for single-user usage with maximum FPS and quality.

## Features

- **Real-time Processing**: High-performance face swapping with GPU acceleration
- **Single User Optimized**: Dedicated resources for one user at a time
- **Professional UI**: Clean, responsive web interface with live video feeds
- **Smart Port Management**: Automatic port detection and conflict resolution
- **Proper Cleanup**: Clean server shutdown and resource management
- **Performance Monitoring**: Real-time statistics and processing metrics

## Project Structure

```
FaceSwapLive/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── config.py                # Configuration settings
├── pipeline.py              # Face swap processing pipeline
├── server.py                # Main Flask-SocketIO server
├── app.py                   # Application entry point
├── templates/               # HTML templates
│   └── index.html          # Main web interface
├── static/                  # Static assets
│   ├── css/
│   │   └── style.css       # Stylesheet
│   └── js/
│       └── app.js          # Client-side JavaScript
└── models/                  # AI model files (auto-created)
```

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Server**:
   ```bash
   python app.py
   ```

3. **Access the Application**:
   - Open your browser to the displayed URL (e.g., http://localhost:5000)
   - Upload a source face image
   - Allow camera access
   - Enjoy real-time face swapping!

## Requirements

- Python 3.8+
- CUDA-compatible GPU (recommended)
- Webcam or video input device
- Modern web browser with WebRTC support

## Performance Notes

- Optimized for single user to maximize performance
- Automatic GPU detection and acceleration
- Smart frame rate adjustment based on processing capability
- Memory-efficient processing pipeline

## Stopping the Server

- Press `Ctrl+C` in the terminal
- Server will automatically cleanup and release ports
- All resources properly freed

## Configuration

Edit `config.py` to customize:
- Server host and port settings
- Processing parameters
- Model paths
- Performance tuning options