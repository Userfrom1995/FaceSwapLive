# Troubleshooting Guide

This guide covers common issues and solutions for Face Swap Live.

## Installation Issues

### Python Version Compatibility

**Problem**: Application fails to start with Python version error.

**Solution**:
```bash
# Check Python version
python --version

# Requires Python 3.8 or higher
# Install compatible version if needed
```

### Dependency Installation Failures

**Problem**: `pip install -r requirements.txt` fails.

**Solutions**:

1. **Update pip**:
   ```bash
   python -m pip install --upgrade pip
   ```

2. **Install with verbose output**:
   ```bash
   pip install -r requirements.txt -v
   ```

3. **Install individually**:
   ```bash
   pip install torch torchvision
   pip install opencv-python
   pip install insightface
   # Continue with other packages
   ```

4. **Use conda environment**:
   ```bash
   conda create -n faceswap python=3.9
   conda activate faceswap
   pip install -r requirements.txt
   ```

### CUDA Installation Issues

**Problem**: GPU not detected or CUDA errors.

**Solutions**:

1. **Verify CUDA installation**:
   ```bash
   nvidia-smi
   nvcc --version
   ```

2. **Install CUDA toolkit**:
   - Download from [NVIDIA CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit)
   - Follow platform-specific installation guide

3. **Install PyTorch with CUDA**:
   ```bash
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   ```

4. **Verify PyTorch CUDA**:
   ```python
   import torch
   print(torch.cuda.is_available())
   print(torch.cuda.get_device_name(0))
   ```

## Model Issues

### Model Download Failures

**Problem**: Models fail to download automatically.

**Solutions**:

1. **Check internet connection**:
   ```bash
   ping github.com
   ```

2. **Manual download**:
   ```bash
   # Download models manually
   wget https://github.com/Userfrom1995/FaceSwapLive/releases/download/v1.0.0/inswapper_128.onnx
   wget https://github.com/Userfrom1995/FaceSwapLive/releases/download/v1.0.0/GFPGANv1.4.pth
   
   # Place in models/ directory
   mv *.onnx *.pth models/
   ```

3. **Check disk space**:
   ```bash
   df -h
   # Ensure at least 2GB free space
   ```

4. **Verify model integrity**:
   ```bash
   # Check file sizes
   ls -lh models/
   # inswapper_128.onnx should be ~530MB
   # GFPGANv1.4.pth should be ~332MB
   ```

### Model Loading Errors

**Problem**: Models fail to load with ONNX or PyTorch errors.

**Solutions**:

1. **Check model files**:
   ```bash
   # Verify files are not corrupted
   file models/*.onnx
   file models/*.pth
   ```

2. **Clear model cache**:
   ```bash
   rm -rf ~/.insightface/
   rm -rf models/*.onnx models/*.pth
   # Restart application to redownload
   ```

3. **Force CPU mode**:
   ```bash
   python app.py --no-gpu
   ```

4. **Update ONNX Runtime**:
   ```bash
   pip install --upgrade onnxruntime-gpu
   # or for CPU only
   pip install --upgrade onnxruntime
   ```

## Server Issues

### Port Already in Use

**Problem**: Server fails to start with "Address already in use" error.

**Solutions**:

1. **Find process using port**:
   ```bash
   # Linux/macOS
   lsof -i :5000
   
   # Windows
   netstat -ano | findstr :5000
   ```

2. **Kill process**:
   ```bash
   # Linux/macOS
   kill -9 PID
   
   # Windows
   taskkill /PID PID /F
   ```

3. **Use different port**:
   ```bash
   python app.py --port 8080
   ```

4. **Let system choose port**:
   ```bash
   python app.py
   # System will find available port automatically
   ```

### Memory Issues

**Problem**: Out of memory errors or system slowdown.

**Solutions**:

1. **Check system resources**:
   ```bash
   # Linux/macOS
   free -h
   nvidia-smi
   
   # Windows
   wmic OS get TotalVisibleMemorySize,FreePhysicalMemory
   ```

2. **Reduce GPU memory limit**:
   ```python
   # In config.py
   GPU_MEMORY_LIMIT = 4 * 1024 * 1024 * 1024  # 4GB instead of 12GB
   ```

3. **Enable frame skipping**:
   ```python
   # In config.py
   FRAME_SKIP_THRESHOLD = 2  # Skip every 2nd frame
   TARGET_FPS = 15  # Reduce target FPS
   ```

4. **Close other applications**:
   - Close browser tabs
   - Stop other GPU-intensive applications
   - Free up system RAM

### Performance Issues

**Problem**: Low FPS or high latency.

**Solutions**:

1. **Check GPU utilization**:
   ```bash
   nvidia-smi -l 1
   # Monitor GPU usage
   ```

2. **Optimize configuration**:
   ```python
   # In config.py
   JPEG_QUALITY = 75  # Reduce from 85
   WEBCAM_WIDTH = 480  # Reduce from 640
   WEBCAM_HEIGHT = 360  # Reduce from 480
   ```

3. **Enable performance mode**:
   ```bash
   python app.py --debug
   # Check performance logs
   ```

4. **Update drivers**:
   - Update NVIDIA GPU drivers
   - Update system drivers
   - Restart system after updates

## Ngrok Issues

### Authentication Failures

**Problem**: "Authentication failed" when starting ngrok tunnel.

**Solutions**:

1. **Verify auth token**:
   ```bash
   # Check token format (should be 40+ characters)
   echo $NGROK_AUTH_TOKEN
   ```

2. **Reconfigure token**:
   ```bash
   ngrok config add-authtoken YOUR_TOKEN_HERE
   ```

3. **Check account status**:
   - Login to [ngrok.com](https://ngrok.com)
   - Verify account is active
   - Check usage limits

### Tunnel Connection Issues

**Problem**: Tunnel fails to start or becomes unreachable.

**Solutions**:

1. **Check ngrok installation**:
   ```bash
   ngrok version
   ```

2. **Test basic tunnel**:
   ```bash
   ngrok http 8000
   # Test with simple HTTP server
   ```

3. **Try different region**:
   ```bash
   python app.py --ngrok --ngrok-region eu
   ```

4. **Check firewall**:
   - Ensure ngrok can access internet
   - Check corporate firewall settings
   - Try different network if possible

### Port Mismatch Issues

**Problem**: "Port mismatch" warnings in logs.

**Solutions**:

1. **Kill existing ngrok processes**:
   ```bash
   pkill -f ngrok
   ```

2. **Restart application**:
   ```bash
   python app.py --ngrok --ngrok-auth-token YOUR_TOKEN
   ```

3. **Check for conflicting tunnels**:
   ```bash
   # Visit ngrok dashboard
   curl http://localhost:4040/api/tunnels
   ```

## Browser Issues

### WebRTC/Camera Issues

**Problem**: Camera not working or permission denied.

**Solutions**:

1. **Check browser permissions**:
   - Allow camera access in browser settings
   - Refresh page after granting permissions

2. **Try different browser**:
   - Chrome (recommended)
   - Firefox
   - Edge

3. **Check HTTPS requirement**:
   - WebRTC requires HTTPS for remote access
   - Use ngrok tunnel for HTTPS
   - Or access via localhost

4. **Test camera separately**:
   ```javascript
   // In browser console
   navigator.mediaDevices.getUserMedia({video: true})
     .then(stream => console.log('Camera works'))
     .catch(err => console.error('Camera error:', err));
   ```

### Connection Issues

**Problem**: WebSocket connection failures or frequent disconnections.

**Solutions**:

1. **Check network stability**:
   ```bash
   ping google.com
   ```

2. **Increase timeouts**:
   ```python
   # In config.py
   PING_TIMEOUT = 120  # Increase from 60
   PING_INTERVAL = 30  # Increase from 25
   ```

3. **Check browser console**:
   - Open Developer Tools (F12)
   - Check Console tab for errors
   - Check Network tab for failed requests

4. **Try different network**:
   - Switch to different WiFi
   - Try mobile hotspot
   - Check corporate network restrictions

## Google Colab Issues

### Session Timeouts

**Problem**: Colab session disconnects or times out.

**Solutions**:

1. **Keep session active**:
   ```javascript
   // Run in browser console to prevent timeout
   setInterval(() => {
     document.querySelector("colab-connect-button").click();
   }, 60000);
   ```

2. **Use Colab Pro**:
   - Longer session limits
   - Better GPU access
   - Priority access

3. **Save work frequently**:
   - Download models before session ends
   - Save configuration changes

### GPU Access Issues

**Problem**: No GPU available in Colab.

**Solutions**:

1. **Enable GPU runtime**:
   - Runtime → Change runtime type
   - Hardware accelerator → GPU
   - Save and reconnect

2. **Check GPU availability**:
   ```python
   import torch
   print(torch.cuda.is_available())
   !nvidia-smi
   ```

3. **Try different times**:
   - GPU availability varies by demand
   - Try during off-peak hours
   - Consider Colab Pro for guaranteed access

### Model Redownload Issues

**Problem**: Models redownload every session.

**Solutions**:

1. **Expected behavior**:
   - Colab sessions are temporary
   - Models must redownload each time
   - This is normal and expected

2. **Speed up downloads**:
   - Use stable internet connection
   - Close unnecessary browser tabs
   - Wait for downloads to complete

## Debug Mode

### Enable Debug Logging

```bash
python app.py --debug
```

This enables:
- Detailed error messages
- Performance metrics
- Model loading information
- Network connection details

### Log Analysis

Check logs for common patterns:

1. **Memory errors**: Look for "CUDA out of memory"
2. **Model errors**: Look for "Failed to load model"
3. **Network errors**: Look for "Connection refused"
4. **Permission errors**: Look for "Permission denied"

### Performance Monitoring

```python
# Check processing statistics
# Visit: http://localhost:PORT/status
{
  "frame_count": 1234,
  "swap_count": 1200,
  "error_count": 34,
  "avg_processing_time": 45.2,
  "source_face_loaded": true,
  "models_loaded": true
}
```

## Getting Help

### Information to Provide

When seeking help, include:

1. **System Information**:
   ```bash
   python --version
   pip list | grep -E "(torch|opencv|insightface)"
   nvidia-smi  # If using GPU
   ```

2. **Error Messages**:
   - Complete error traceback
   - Browser console errors
   - System logs

3. **Configuration**:
   - Command line arguments used
   - Environment variables set
   - Custom configuration changes

4. **Steps to Reproduce**:
   - Exact steps that cause the issue
   - Expected vs actual behavior
   - Frequency of occurrence

### Support Channels

- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: Check `docs/` directory
- **Debug Mode**: Use `--debug` flag for detailed logs
- **Community**: GitHub Discussions for questions

### Self-Help Tools

1. **Test Scripts**:
   ```bash
   python test_models.py
   python test_port_coordination.py
   python debug_pipeline.py
   ```

2. **Interactive Setup**:
   ```bash
   python ngrok_setup.py
   ```

3. **Configuration Validation**:
   ```bash
   python -c "from config import config; print('Config loaded successfully')"
   ```