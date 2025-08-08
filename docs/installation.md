# Installation

## Requirements
- Python 3.8+
- Internet connection (for model downloads)
- Optional: NVIDIA GPU with CUDA for better performance

## Local Installation

```bash
git clone https://github.com/Userfrom1995/FaceSwapLive.git
cd FaceSwapLive
pip install -r requirements.txt
python app.py
```

Open the displayed URL in your browser.

## Google Colab

1. Open: https://colab.research.google.com/github/Userfrom1995/FaceSwapLive/blob/main/FaceSwapLive.ipynb
2. Run all cells
3. Replace the ngrok token placeholder with your token from https://dashboard.ngrok.com

## GPU vs CPU

**GPU mode** (default): Faster processing, requires NVIDIA GPU with CUDA
**CPU mode**: Slower but works on any system
```bash
python app.py --no-gpu
```

## Models

Two models download automatically on first run:
- `inswapper_128.onnx` (530MB) - Face swapping
- `GFPGANv1.4.pth` (332MB) - Face enhancement

If download fails, get them manually from `models/instructions.txt`

## Next Steps

- **Public Access**: See [Ngrok Setup](ngrok.md)
- **Command Line Options**: See [Arguments Reference](arguments.md)
- **Configuration**: See [Configuration Reference](configuration.md)
- **Issues**: See [Troubleshooting](troubleshooting.md)