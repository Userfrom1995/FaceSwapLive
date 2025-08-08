# Face Swap Live

A high-performance, real-time face swapping application with web interface and public access capabilities.

## Overview

Face Swap Live provides real-time face swapping through a web browser interface. The application features GPU acceleration, automatic model management, and integrated ngrok support for public access. It's designed for both local development and cloud deployment (Google Colab).

## Features

- **Real-time Processing**: GPU-accelerated face swapping with optimized performance
- **Web Interface**: Browser-based interface accessible from any device
- **Public Access**: Integrated ngrok support for sharing and remote access
- **Automatic Setup**: Models download automatically on first run
- **Cloud Ready**: Full Google Colab support with one-click deployment
- **Professional Grade**: Enterprise-ready codebase with comprehensive logging

## Quick Start

### Local Installation

```bash
git clone https://github.com/Userfrom1995/FaceSwapLive.git
cd FaceSwapLive
pip install -r requirements.txt
python app.py
```

### Google Colab

Open the notebook directly in Colab:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Userfrom1995/FaceSwapLive/blob/main/FaceSwapLive.ipynb)

### Public Access (Ngrok)

```bash
python app.py --ngrok --ngrok-auth-token YOUR_TOKEN
```

## Project Structure

```
FaceSwapLive/
├── app.py                 # Main application entry point
├── server.py              # Optimized Flask server
├── pipeline.py            # Face processing pipeline
├── models.py              # Model management and downloading
├── config.py              # Configuration management
├── ngrok_manager.py       # Ngrok tunnel management
├── FaceSwapLive.ipynb     # Google Colab notebook
├── models/                # AI models directory
│   └── instructions.txt   # Model setup instructions
├── templates/             # Web interface templates
├── static/                # Static assets (CSS, JS)
├── docs/                  # Documentation
└── requirements.txt       # Python dependencies
```

## AI Models

Face Swap Live uses two AI models that download automatically:

- **inswapper_128.onnx** (530MB) - Face swapping model
- **GFPGANv1.4.pth** (332MB) - Face enhancement model

Manual download instructions are available in `models/instructions.txt`.

## Hardware Requirements

### Recommended
- GPU: 4GB+ VRAM (NVIDIA with CUDA support)
- RAM: 8GB+
- Storage: 2GB free space

### Minimum
- GPU: 2GB VRAM or CPU processing
- RAM: 4GB
- Storage: 1GB free space

## Usage

### Basic Usage
1. Start server: `python app.py`
2. Open browser to displayed URL
3. Upload source face image
4. Enable webcam for real-time face swapping

### Public Access
1. Get ngrok auth token from [ngrok.com](https://ngrok.com)
2. Run: `python app.py --ngrok --ngrok-auth-token YOUR_TOKEN`
3. Share the generated public URL

### Google Colab
1. Open notebook in Colab
2. Execute all cells in order
3. Replace auth token placeholder with your token
4. Access via generated public URL

## Configuration

Configuration is managed through `config.py`. Key settings:

- **Server**: Host, port, and performance settings
- **Processing**: Frame rate, quality, and optimization
- **Models**: Model paths and download URLs
- **Ngrok**: Tunnel configuration and security
- **Security**: Rate limiting and access control

## Documentation

- [Installation](docs/installation.md) - Setup instructions
- [Ngrok Setup](docs/ngrok.md) - Public access configuration
- [Arguments Reference](docs/arguments.md) - Command line options
- [Configuration](docs/configuration.md) - Configuration options
- [API Reference](docs/api-reference.md) - Server endpoints and WebSocket events
- [Troubleshooting](docs/troubleshooting.md) - Common issues and solutions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the AGPL-3.0 License. See [LICENSE](LICENSE) for details.

## Inspiration

The idea for Face Swap Live came from a simple need: most face swapping applications I found were GUI-based desktop applications that were difficult to set up and configure. I wanted something web-based that would be easy to set up and quick to use - just for fun! That's where it all began.

The goal was to create a simple, accessible face swapping experience that anyone could use through their browser without complex installation procedures.

## Credits

This project uses AI models and libraries from the open-source community:

- **[InsightFace](https://github.com/deepinsight/insightface)** - Face analysis and detection models
- **[GFPGAN](https://github.com/TencentARC/GFPGAN)** - Face enhancement technology
- **Flask & SocketIO** - Web framework and real-time communication
- **ONNX Runtime** - Model inference optimization

All models and libraries are used in accordance with their respective licenses.

## Support

- **Issues**: Report bugs and feature requests via GitHub Issues
- **Documentation**: Check the `docs/` directory for detailed guides
- **Community**: Join discussions in GitHub Discussions

---

**Note**: This application is for educational and research purposes. Please ensure you have proper consent when using face swapping technology with other people's images.