# 🌐 Ngrok Integration for Face Swap Live

Face Swap Live now supports ngrok tunnels for easy public access and sharing!

## 🚀 Quick Start

### 1. Install ngrok
```bash
# Visit https://ngrok.com/download or use package managers:
# Windows
choco install ngrok

# macOS  
brew install ngrok/ngrok/ngrok

# Linux
snap install ngrok
```

### 2. Get Auth Token
1. Sign up at [ngrok.com](https://ngrok.com)
2. Get your auth token from [dashboard](https://dashboard.ngrok.com/get-started/your-authtoken)

### 3. Run Setup (Optional)
```bash
python ngrok_setup.py
```

### 4. Start with Ngrok
```bash
# Basic usage
python app.py --ngrok --ngrok-auth-token YOUR_TOKEN

# Or set environment variable
export NGROK_AUTH_TOKEN=your_token_here
python app.py --ngrok
```

## 📋 Command Line Options

```bash
# Enable ngrok tunnel
python app.py --ngrok

# With auth token
python app.py --ngrok --ngrok-auth-token YOUR_TOKEN

# Custom subdomain (paid plan required)
python app.py --ngrok --ngrok-subdomain myapp

# Different region
python app.py --ngrok --ngrok-region eu

# Complete example
python app.py --ngrok --ngrok-auth-token abc123 --ngrok-subdomain faceswap --ngrok-region us
```

## 🌍 Available Regions

- `us` - United States (default)
- `eu` - Europe  
- `ap` - Asia Pacific
- `au` - Australia
- `sa` - South America
- `jp` - Japan
- `in` - India

## 🔧 Environment Variables

Create a `.env` file or set these environment variables:

```bash
NGROK_AUTH_TOKEN=your_token_here
NGROK_SUBDOMAIN=your-custom-subdomain  # Optional, paid plan required
NGROK_REGION=us                        # Optional, default is 'us'
```

## 💡 Use Cases

### 🎯 Remote Access
Access your Face Swap Live server from anywhere:
```bash
python app.py --ngrok
# Share the generated URL with yourself for remote access
```

### 🎪 Demos & Presentations  
Share your server with others for demos:
```bash
python app.py --ngrok --ngrok-subdomain demo-faceswap
# Professional URL: https://demo-faceswap.ngrok.io
```

### 👥 Team Collaboration
Let team members access your development server:
```bash
python app.py --ngrok --debug
# Share the URL with your team
```

### 🌐 Testing on Mobile
Test your app on mobile devices:
```bash
python app.py --ngrok
# Open the ngrok URL on your phone
```

## ⚠️ Security Considerations

### 🔒 Important Warnings
- **Public Access**: Ngrok makes your server publicly accessible
- **No Authentication**: Anyone with the URL can access your server  
- **Rate Limiting**: Consider the security settings in `config.py`
- **Temporary URLs**: Free ngrok URLs change on restart

### 🛡️ Best Practices
1. **Don't share URLs publicly** - Only with trusted users
2. **Use custom subdomains** for professional demos (paid plan)
3. **Monitor usage** - Check ngrok dashboard for traffic
4. **Restart regularly** - URLs change, limiting exposure
5. **Consider authentication** - Add your own auth layer if needed

## 🔧 Troubleshooting

### Common Issues

**"ngrok not found"**
```bash
# Make sure ngrok is installed and in PATH
ngrok version
```

**"Authentication failed"**
```bash
# Configure your auth token
ngrok config add-authtoken YOUR_TOKEN
```

**"Tunnel failed to start"**
- Check if port is already in use
- Verify auth token is correct
- Try different region: `--ngrok-region eu`

**"Subdomain not available"**
- Custom subdomains require paid plan
- Try different subdomain name
- Remove `--ngrok-subdomain` for random URL

### Debug Mode
```bash
# Enable debug logging
python app.py --ngrok --debug
```

## 📊 Monitoring

### Ngrok Dashboard
- Visit: http://localhost:4040 (when tunnel is active)
- View traffic, requests, and tunnel status
- Replay requests for debugging

### Application Logs
The app will show ngrok status in logs:
```
✅ Ngrok tunnel active: https://abc123.ngrok.io
🌐 Opened tunnel URL in browser
```

## 🆙 Upgrading to Paid Plans

Free ngrok includes:
- ✅ HTTPS tunnels
- ✅ Random subdomains  
- ✅ Basic traffic inspection
- ❌ Custom subdomains
- ❌ Reserved domains
- ❌ Multiple tunnels

Paid plans add:
- ✅ Custom subdomains
- ✅ Reserved domains
- ✅ Multiple simultaneous tunnels
- ✅ Advanced traffic inspection
- ✅ Team collaboration features

## 🤝 Support

If you encounter issues:
1. Check the [ngrok documentation](https://ngrok.com/docs)
2. Run `python ngrok_setup.py` for guided setup
3. Enable debug mode: `python app.py --ngrok --debug`
4. Check ngrok dashboard at http://localhost:4040

---

**Happy face swapping! 🎭✨**