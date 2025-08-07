#!/usr/bin/env python3
"""
Ngrok Setup Utility for Face Swap Live

This utility helps users set up ngrok for their Face Swap Live server.
It provides an interactive setup process and validates the configuration.
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header():
    """Print setup header"""
    print("\n" + "="*60)
    print("🌐 FACE SWAP LIVE - NGROK SETUP")
    print("="*60)
    print("This utility will help you set up ngrok for public access")
    print("to your Face Swap Live server.")
    print()

def check_ngrok_installation():
    """Check if ngrok is installed"""
    print("🔍 Checking ngrok installation...")
    try:
        result = subprocess.run(['ngrok', 'version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Ngrok is installed: {version}")
            return True
        else:
            print("❌ Ngrok is installed but not working properly")
            return False
    except FileNotFoundError:
        print("❌ Ngrok is not installed or not in PATH")
        print("\n💡 To install ngrok:")
        print("   1. Visit: https://ngrok.com/download")
        print("   2. Download ngrok for your platform")
        print("   3. Extract and add to your PATH")
        print("   4. Or use package managers:")
        print("      - Windows: choco install ngrok")
        print("      - macOS: brew install ngrok/ngrok/ngrok")
        print("      - Linux: snap install ngrok")
        return False
    except subprocess.TimeoutExpired:
        print("❌ Ngrok command timed out")
        return False

def get_auth_token():
    """Get ngrok auth token from user"""
    print("\n🔑 Ngrok Authentication Setup")
    print("To use ngrok, you need a free account and auth token.")
    print("1. Sign up at: https://ngrok.com")
    print("2. Go to: https://dashboard.ngrok.com/get-started/your-authtoken")
    print("3. Copy your auth token")
    print()
    
    # Check if token is already configured
    try:
        config_path = Path.home() / ".ngrok2" / "ngrok.yml"
        if config_path.exists():
            print("✅ Ngrok config file found, auth token may already be configured")
            use_existing = input("Use existing configuration? (y/n): ").lower().strip()
            if use_existing == 'y':
                return None  # Use existing config
    except Exception:
        pass
    
    while True:
        token = input("Enter your ngrok auth token (or 'skip' to use existing): ").strip()
        
        if token.lower() == 'skip':
            return None
        
        if len(token) < 10:
            print("❌ Auth token seems too short. Please check and try again.")
            continue
        
        # Test the token
        print("🔄 Testing auth token...")
        try:
            result = subprocess.run(['ngrok', 'config', 'add-authtoken', token],
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ Auth token configured successfully!")
                return token
            else:
                print(f"❌ Failed to configure auth token: {result.stderr}")
                retry = input("Try again? (y/n): ").lower().strip()
                if retry != 'y':
                    return None
        except Exception as e:
            print(f"❌ Error testing auth token: {e}")
            return None

def test_tunnel():
    """Test ngrok tunnel functionality"""
    print("\n🧪 Testing ngrok tunnel...")
    print("This will start a test tunnel on port 8000 for 10 seconds...")
    
    try:
        # Start a simple test server
        import http.server
        import socketserver
        import threading
        import time
        
        # Start test HTTP server
        handler = http.server.SimpleHTTPRequestHandler
        httpd = socketserver.TCPServer(("", 8000), handler)
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        
        print("🚀 Starting test tunnel...")
        process = subprocess.Popen(['ngrok', 'http', '8000'], 
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a bit for ngrok to start
        time.sleep(3)
        
        # Try to get tunnel URL
        try:
            import requests
            response = requests.get("http://localhost:4040/api/tunnels", timeout=2)
            if response.status_code == 200:
                data = response.json()
                tunnels = data.get('tunnels', [])
                if tunnels:
                    url = tunnels[0].get('public_url')
                    print(f"✅ Test tunnel active: {url}")
                    print("🎉 Ngrok is working correctly!")
                else:
                    print("⚠️  Tunnel started but no URL found")
            else:
                print("⚠️  Could not get tunnel info from ngrok API")
        except Exception as e:
            print(f"⚠️  Could not verify tunnel: {e}")
        
        # Clean up
        time.sleep(2)
        process.terminate()
        httpd.shutdown()
        print("🛑 Test tunnel stopped")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def create_env_file(auth_token):
    """Create .env file with ngrok configuration"""
    if not auth_token:
        return
    
    env_file = Path(".env")
    env_content = f"""# Ngrok Configuration for Face Swap Live
NGROK_AUTH_TOKEN={auth_token}
# NGROK_SUBDOMAIN=your-custom-subdomain  # Uncomment for paid plans
# NGROK_REGION=us  # Options: us, eu, ap, au, sa, jp, in
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print(f"✅ Created {env_file} with ngrok configuration")
        print("💡 You can now use: python app.py --ngrok")
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")

def main():
    """Main setup function"""
    print_header()
    
    # Check ngrok installation
    if not check_ngrok_installation():
        print("\n❌ Setup cannot continue without ngrok installed")
        sys.exit(1)
    
    # Get auth token
    auth_token = get_auth_token()
    
    # Test tunnel
    if input("\nTest ngrok tunnel? (y/n): ").lower().strip() == 'y':
        test_tunnel()
    
    # Create env file
    if auth_token:
        create_env_file(auth_token)
    
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETE!")
    print("="*60)
    print("You can now start Face Swap Live with ngrok:")
    print("  python app.py --ngrok")
    print()
    print("Or with custom options:")
    print("  python app.py --ngrok --ngrok-region eu")
    print("  python app.py --ngrok --ngrok-subdomain myapp")
    print()
    print("⚠️  Security Warning:")
    print("   Ngrok makes your server publicly accessible!")
    print("   Only share the URL with trusted users.")
    print("="*60)

if __name__ == "__main__":
    main()