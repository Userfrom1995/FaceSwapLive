# Command Line Arguments

Complete reference for Face Swap Live command line arguments.

## Basic Usage

```bash
python app.py [OPTIONS]
```

## Server Arguments

### --host HOST
**Description**: Server host address
**Default**: `0.0.0.0` (all interfaces)
**Example**: 
```bash
python app.py --host 127.0.0.1  # localhost only
python app.py --host 0.0.0.0    # all interfaces
```

### --port PORT
**Description**: Server port number
**Default**: Auto-detected (random available port)
**Example**:
```bash
python app.py --port 8080
```

### --debug
**Description**: Enable debug mode
**Default**: Disabled
**Effect**: 
- Enables detailed logging
- Shows performance metrics
- Displays model loading information
**Example**:
```bash
python app.py --debug
```

## GPU Arguments

### --no-gpu
**Description**: Disable GPU acceleration
**Default**: GPU enabled (if available)
**Effect**: Forces CPU-only processing
**Example**:
```bash
python app.py --no-gpu
```

## Model Arguments

### --models-dir PATH
**Description**: Custom models directory path
**Default**: `./models`
**Example**:
```bash
python app.py --models-dir /path/to/models
```

## Ngrok Arguments

### --ngrok
**Description**: Enable ngrok tunnel for public access
**Default**: Disabled
**Example**:
```bash
python app.py --ngrok --ngrok-auth-token YOUR_TOKEN
```

### --ngrok-auth-token TOKEN
**Description**: Ngrok authentication token
**Required**: When using `--ngrok`
**Priority**: Highest (overrides environment variables)
**Example**:
```bash
python app.py --ngrok --ngrok-auth-token abc123def456
```

### --ngrok-subdomain NAME
**Description**: Custom ngrok subdomain
**Default**: Random subdomain
**Requirement**: Paid ngrok plan
**Example**:
```bash
python app.py --ngrok --ngrok-auth-token TOKEN --ngrok-subdomain myapp
# Results in: https://myapp.ngrok.io
```

### --ngrok-region REGION
**Description**: Ngrok server region
**Default**: `us`
**Options**: `us`, `eu`, `ap`, `au`, `sa`, `jp`, `in`
**Example**:
```bash
python app.py --ngrok --ngrok-auth-token TOKEN --ngrok-region eu
```

## Complete Examples

### Local development
```bash
python app.py --debug
```

### Local with specific port
```bash
python app.py --port 8080 --debug
```

### CPU-only mode
```bash
python app.py --no-gpu
```

### Public access with ngrok
```bash
python app.py --ngrok --ngrok-auth-token YOUR_TOKEN
```

### Professional demo setup
```bash
python app.py --ngrok \
  --ngrok-auth-token YOUR_TOKEN \
  --ngrok-subdomain faceswap-demo \
  --ngrok-region us \
  --port 5000
```

### Custom models directory
```bash
python app.py --models-dir /custom/path/models --debug
```

### Complete production setup
```bash
python app.py \
  --host 0.0.0.0 \
  --port 5000 \
  --ngrok \
  --ngrok-auth-token YOUR_TOKEN \
  --ngrok-region eu \
  --models-dir /opt/faceswap/models
```

## Argument Combinations

### Development
```bash
python app.py --debug --no-gpu --port 8080
```

### Testing
```bash
python app.py --debug --models-dir ./test-models
```

### Demo/Presentation
```bash
python app.py --ngrok --ngrok-auth-token TOKEN --ngrok-subdomain demo
```

### Production
```bash
python app.py --host 0.0.0.0 --port 5000 --ngrok --ngrok-auth-token TOKEN
```

## Help

### View all arguments
```bash
python app.py --help
```

### Argument validation
- Invalid arguments will show error message
- Use `--help` to see all available options
- Arguments are validated on startup