# Ngrok Setup Guide

This guide covers setting up ngrok for public access to your Face Swap Live server.

## Overview

Ngrok creates secure tunnels to localhost, allowing you to share your Face Swap Live server publicly without complex network configuration. This is particularly useful for:

- Remote access to your server
- Sharing with team members
- Testing on mobile devices
- Cloud deployment (Google Colab)
- Demonstrations and presentations

## Installation

### Method 1: Package Managers

**Windows (Chocolatey)**:
```bash
choco install ngrok
```

**macOS (Homebrew)**:
```bash
brew install ngrok/ngrok/ngrok
```

**Linux (Snap)**:
```bash
snap install ngrok
```

### Method 2: Manual Installation

1. Visit [ngrok.com/download](https://ngrok.com/download)
2. Download the appropriate version for your platform
3. Extract the executable
4. Add to your system PATH

### Verification

Verify installation:
```bash
ngrok version
```

## Authentication Setup

### Get Auth Token

1. Sign up at [ngrok.com](https://ngrok.com) (free account)
2. Navigate to [dashboard](https://dashboard.ngrok.com/get-started/your-authtoken)
3. Copy your authentication token

### Configure Token

**Method 1: Command Line**
```bash
ngrok config add-authtoken YOUR_TOKEN_HERE
```

**Method 2: Environment Variable**
```bash
export NGROK_AUTH_TOKEN=YOUR_TOKEN_HERE
```

**Method 3: .env File**
```bash
echo "NGROK_AUTH_TOKEN=YOUR_TOKEN_HERE" > .env
```

## Usage with Face Swap Live

### Basic Usage

Start server with ngrok tunnel:
```bash
python app.py --ngrok --ngrok-auth-token YOUR_TOKEN
```

### Environment Variable Method

Set token once:
```bash
export NGROK_AUTH_TOKEN=YOUR_TOKEN
python app.py --ngrok
```

### Advanced Options

**Custom Subdomain** (requires paid plan):
```bash
python app.py --ngrok --ngrok-subdomain faceswap-demo
```

**Different Region**:
```bash
python app.py --ngrok --ngrok-region eu
```

**Complete Example**:
```bash
python app.py --ngrok --ngrok-auth-token abc123 --ngrok-subdomain demo --ngrok-region us
```

## Available Regions

- `us` - United States (default)
- `eu` - Europe
- `ap` - Asia Pacific
- `au` - Australia
- `sa` - South America
- `jp` - Japan
- `in` - India

## Interactive Setup

Use the interactive setup utility:
```bash
python ngrok_setup.py
```

This utility will:
- Verify ngrok installation
- Configure authentication token
- Test tunnel functionality
- Create configuration files

## Port Coordination

Face Swap Live automatically coordinates ports between the server and ngrok tunnel:

1. **Dynamic Port Detection**: Server finds available port
2. **Tunnel Creation**: Ngrok tunnel created for exact port
3. **Verification**: System verifies tunnel points to correct port
4. **Server Start**: Server starts on coordinated port

### Port Architecture

```
Internet → https://abc123.ngrok.io → localhost:DYNAMIC_PORT (your server)
                                           ↑
                                   Monitor via localhost:4040 (ngrok dashboard)
```

## Monitoring and Debugging

### Ngrok Dashboard

Access the local dashboard at `http://localhost:4040` when tunnel is active:

- **Traffic Inspection**: View all HTTP requests
- **Request Replay**: Replay requests for debugging
- **Tunnel Status**: Monitor tunnel health
- **Performance Metrics**: Bandwidth and latency stats

### Application Logs

Face Swap Live provides detailed ngrok logging:

```
[12:34:56] INFO: Starting ngrok tunnel for port 3005...
[12:34:57] INFO: Ngrok tunnel active: https://abc123.ngrok.io
[12:34:57] INFO: Tunnel verified: https://abc123.ngrok.io -> localhost:3005
```

## Configuration Options

### Configuration Priority

Face Swap Live uses a hierarchical configuration system with the following priority (highest to lowest):

1. **Command Line Arguments** (highest priority)
2. **Environment Variables** (medium priority)
3. **`.env` File** (lowest priority)

### Environment Variables

```bash
NGROK_AUTH_TOKEN=your_token_here
NGROK_SUBDOMAIN=your-custom-subdomain  # Optional, paid plan required
NGROK_REGION=us                        # Optional, default is 'us'
NGROK_DASHBOARD_PORT=4040              # Optional, default is 4040
```

### Command Line Arguments

```bash
--ngrok                    # Enable ngrok tunnel
--ngrok-auth-token TOKEN   # Authentication token (highest priority)
--ngrok-subdomain NAME     # Custom subdomain (paid plan)
--ngrok-region REGION      # Tunnel region
```

### Priority Examples

```bash
# Example 1: Command line overrides everything
echo "NGROK_AUTH_TOKEN=file_token" > .env
export NGROK_AUTH_TOKEN=env_token
python app.py --ngrok --ngrok-auth-token cmd_token
# Result: Uses "cmd_token" (command line wins)

# Example 2: Environment variable overrides .env file
echo "NGROK_AUTH_TOKEN=file_token" > .env
export NGROK_AUTH_TOKEN=env_token
python app.py --ngrok
# Result: Uses "env_token" (environment variable wins)

# Example 3: .env file as fallback
echo "NGROK_AUTH_TOKEN=file_token" > .env
python app.py --ngrok
# Result: Uses "file_token" (.env file used as default)
```

## Security Considerations

### Important Warnings

- **Public Access**: Ngrok makes your server publicly accessible
- **No Authentication**: Anyone with the URL can access your server
- **Temporary URLs**: Free ngrok URLs change on restart
- **Rate Limiting**: Consider implementing rate limiting

### Best Practices

1. **Limited Sharing**: Only share URLs with trusted users
2. **Custom Subdomains**: Use paid plan for professional demos
3. **Regular Monitoring**: Check ngrok dashboard for traffic
4. **Session Management**: Restart regularly to change URLs
5. **Access Logging**: Monitor who accesses your server

### Rate Limiting

Face Swap Live includes built-in rate limiting:
- Maximum 15 frames per second per user
- Session timeout after 5 minutes of inactivity
- Single user mode enforcement

## Troubleshooting

### Common Issues

**"ngrok not found"**
- Ensure ngrok is installed and in PATH
- Verify installation: `ngrok version`

**"Authentication failed"**
- Verify auth token is correct
- Reconfigure: `ngrok config add-authtoken YOUR_TOKEN`

**"Tunnel failed to start"**
- Check if port is already in use
- Try different region: `--ngrok-region eu`
- Verify internet connection

**"Subdomain not available"**
- Custom subdomains require paid plan
- Try different subdomain name
- Remove `--ngrok-subdomain` for random URL

**"Port mismatch"**
- Restart the application
- Kill existing ngrok processes: `pkill -f ngrok`
- Check for conflicting tunnels

### Debug Mode

Enable debug logging:
```bash
python app.py --ngrok --debug
```

### Manual Tunnel Testing

Test ngrok independently:
```bash
ngrok http 8000
```

## Free vs Paid Plans

### Free Plan Includes
- HTTPS tunnels
- Random subdomains
- Basic traffic inspection
- 1 online ngrok process

### Paid Plans Add
- Custom subdomains
- Reserved domains
- Multiple simultaneous tunnels
- Advanced traffic inspection
- Team collaboration features
- Higher bandwidth limits

## Google Colab Integration

The Face Swap Live notebook automatically handles ngrok setup:

1. **Token Input**: Replace placeholder with your token
2. **Automatic Setup**: Tunnel created automatically
3. **Public Access**: Generated URL works immediately
4. **Browser Integration**: Automatically opens in browser

### Colab-Specific Considerations

- **Session Limits**: Colab sessions have time limits
- **Resource Sharing**: GPU resources are shared
- **Network Stability**: Connection may vary
- **Data Persistence**: Models redownload on session restart

## Advanced Configuration

### Custom Dashboard Port

```python
# In config.py
NGROK_DASHBOARD_PORT = 4041
```

### Multiple Tunnels

For paid plans, you can run multiple tunnels:
```bash
ngrok http 3000 --subdomain app1
ngrok http 3001 --subdomain app2
```

### Configuration File

Create `~/.ngrok2/ngrok.yml`:
```yaml
authtoken: YOUR_TOKEN_HERE
region: us
tunnels:
  faceswap:
    proto: http
    addr: 3000
    subdomain: faceswap-demo
```

## Integration with CI/CD

For automated deployments:
```bash
# Set token in environment
export NGROK_AUTH_TOKEN=$NGROK_TOKEN

# Start with automation-friendly options
python app.py --ngrok --no-browser
```

## Support and Resources

- **Ngrok Documentation**: [ngrok.com/docs](https://ngrok.com/docs)
- **Interactive Setup**: `python ngrok_setup.py`
- **Debug Mode**: `python app.py --ngrok --debug`
- **Dashboard**: `http://localhost:4040`