# Ngrok Setup

Ngrok creates secure tunnels to make your local Face Swap Live server publicly accessible.

## Prerequisites

1. **Install ngrok**: Download from https://ngrok.com/download
2. **Get auth token**: Sign up at https://ngrok.com and get your token from https://dashboard.ngrok.com/get-started/your-authtoken

## Basic Usage

```bash
python app.py --ngrok --ngrok-auth-token YOUR_TOKEN
```

## Authentication Token Priority

The system uses this priority order (highest to lowest):

1. **Command Line Argument** (highest priority)
   ```bash
   python app.py --ngrok --ngrok-auth-token YOUR_TOKEN
   ```

2. **Environment Variable** (medium priority)
   ```bash
   export NGROK_AUTH_TOKEN=YOUR_TOKEN
   python app.py --ngrok
   ```

3. **`.env` File** (lowest priority)
   ```bash
   echo "NGROK_AUTH_TOKEN=YOUR_TOKEN" > .env
   python app.py --ngrok
   ```

## Configuration Options

### Command Line Arguments
```bash
--ngrok                    # Enable ngrok tunnel
--ngrok-auth-token TOKEN   # Authentication token
--ngrok-subdomain NAME     # Custom subdomain (paid plan required)
--ngrok-region REGION      # Server region
```

### Environment Variables
```bash
NGROK_AUTH_TOKEN=your_token_here
NGROK_SUBDOMAIN=your-custom-subdomain  # Optional, paid plan required
NGROK_REGION=us                        # Optional, default is 'us'
```

### Available Regions
- `us` - United States (default)
- `eu` - Europe
- `ap` - Asia Pacific
- `au` - Australia
- `sa` - South America
- `jp` - Japan
- `in` - India

## Examples

### Basic tunnel
```bash
python app.py --ngrok --ngrok-auth-token abc123
```

### Custom subdomain (paid plan)
```bash
python app.py --ngrok --ngrok-auth-token abc123 --ngrok-subdomain myapp
```

### Different region
```bash
python app.py --ngrok --ngrok-auth-token abc123 --ngrok-region eu
```

### Using environment variables
```bash
export NGROK_AUTH_TOKEN=abc123
export NGROK_REGION=eu
python app.py --ngrok
```

### Using .env file
Create `.env` file:
```
NGROK_AUTH_TOKEN=abc123
NGROK_SUBDOMAIN=myapp
NGROK_REGION=us
```

Then run:
```bash
python app.py --ngrok
```

## How It Works

1. **Port Detection**: Server finds available port (e.g., 3005)
2. **Tunnel Creation**: Ngrok creates tunnel to that exact port
3. **Verification**: System verifies tunnel points to correct port
4. **Public Access**: Generated URL forwards to your local server

Example output:
```
[12:34:56] INFO: Found available port: 3005
[12:34:57] INFO: Starting ngrok tunnel for port 3005...
[12:34:58] INFO: Ngrok tunnel active: https://abc123.ngrok.io
[12:34:58] INFO: Tunnel verified: https://abc123.ngrok.io -> localhost:3005
```

## Monitoring

### Ngrok Dashboard
- Access at `http://localhost:4040` when tunnel is active
- View traffic, requests, and tunnel status
- Replay requests for debugging

### Application Status
- Check server status at `http://localhost:PORT/status`
- Monitor performance metrics
- View processing statistics

## Security Notes

- **Public Access**: Anyone with the URL can access your server
- **Temporary URLs**: Free ngrok URLs change on restart
- **Rate Limiting**: Built-in rate limiting (15 frames/second per user)
- **Session Timeout**: Automatic cleanup after 5 minutes of inactivity

## Troubleshooting

**Authentication failed**
- Verify token: `echo $NGROK_AUTH_TOKEN`
- Reconfigure: `ngrok config add-authtoken YOUR_TOKEN`

**Tunnel fails to start**
- Check installation: `ngrok version`
- Try different region: `--ngrok-region eu`

**Port mismatch warnings**
- Kill existing processes: `pkill -f ngrok`
- Restart application

**Subdomain not available**
- Custom subdomains require paid plan
- Try different subdomain name
- Remove `--ngrok-subdomain` for random URL