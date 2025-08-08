# Troubleshooting

## Installation Issues

**Python version error**
- Requires Python 3.8+
- Check: `python --version`

**Dependency installation fails**
- Update pip: `python -m pip install --upgrade pip`
- Try: `pip install -r requirements.txt -v`

**CUDA not found**
- Install CUDA toolkit from NVIDIA website
- Or use CPU mode: `python app.py --no-gpu`
- Verify: `nvidia-smi`

## Model Issues

**Models fail to download**
- Check internet connection
- Download manually from `models/instructions.txt`
- Ensure 2GB+ free disk space

**Model loading errors**
- Delete and redownload: `rm -rf models/*.onnx models/*.pth`
- Try CPU mode: `python app.py --no-gpu`
- Update ONNX Runtime: `pip install --upgrade onnxruntime-gpu`

## Server Issues

**Port already in use**
- App automatically finds available port
- Or specify: `python app.py --port 8080`

**Low performance**
- Check GPU usage: `nvidia-smi`
- Use debug mode: `python app.py --debug`
- Close other applications

**Out of memory**
- Reduce GPU memory limit in `config.py`
- Use CPU mode: `python app.py --no-gpu`

## Ngrok Issues

**Authentication failed**
- Verify token: `echo $NGROK_AUTH_TOKEN`
- Reconfigure: `ngrok config add-authtoken YOUR_TOKEN`

**Tunnel fails to start**
- Check ngrok installation: `ngrok version`
- Try different region: `python app.py --ngrok --ngrok-region eu`

**Port mismatch warnings**
- Kill existing processes: `pkill -f ngrok`
- Restart application

## Browser Issues

**Camera not working**
- Allow camera permissions in browser
- Use Chrome (recommended)
- For remote access, use ngrok (HTTPS required)

**Connection issues**
- Check network stability
- Try different browser
- Check browser console (F12) for errors

## Google Colab Issues

**Session timeouts**
- Normal behavior for free accounts
- Consider Colab Pro for longer sessions

**No GPU available**
- Runtime → Change runtime type → GPU
- Try during off-peak hours

**Models redownload each session**
- Normal behavior - Colab sessions are temporary

## Debug Commands

```bash
# Test configuration
python -c "from config import config; print('Config OK')"

# Test models
python test_models.py

# Check status
curl http://localhost:PORT/status

# Enable debug mode
python app.py --debug
```