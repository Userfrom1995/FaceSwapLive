"""
Ngrok Manager for Face Swap Live

Provides easy ngrok integration for exposing the local server to the internet.
Handles authentication, tunnel management, and provides user-friendly URLs.
"""

import os
import logging
import subprocess
import json
import time
import requests
from typing import Optional, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)

class NgrokManager:
    """Manages ngrok tunnels for Face Swap Live server"""
    
    def __init__(self):
        self.tunnel_url: Optional[str] = None
        self.process: Optional[subprocess.Popen] = None
        self.api_url = "http://localhost:4040/api/tunnels"
        
    def is_ngrok_installed(self) -> bool:
        """Check if ngrok is installed and accessible"""
        try:
            result = subprocess.run(['ngrok', 'version'], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def setup_auth_token(self, auth_token: str) -> bool:
        """Setup ngrok authentication token"""
        try:
            result = subprocess.run(['ngrok', 'config', 'add-authtoken', auth_token],
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                logger.info("✅ Ngrok auth token configured successfully")
                return True
            else:
                logger.error(f"❌ Failed to configure auth token: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"❌ Error configuring auth token: {e}")
            return False
    
    def start_tunnel(self, port: int, auth_token: Optional[str] = None, 
                    subdomain: Optional[str] = None, region: str = "us") -> Optional[str]:
        """
        Start ngrok tunnel for the given port
        
        Args:
            port: Local port to expose
            auth_token: Ngrok auth token (optional if already configured)
            subdomain: Custom subdomain (requires paid plan)
            region: Ngrok region (us, eu, ap, au, sa, jp, in)
            
        Returns:
            Public URL if successful, None otherwise
        """
        if not self.is_ngrok_installed():
            logger.error("❌ Ngrok is not installed or not in PATH")
            logger.info("💡 Install ngrok from: https://ngrok.com/download")
            return None
        
        # Setup auth token if provided
        if auth_token:
            if not self.setup_auth_token(auth_token):
                return None
        
        # Build ngrok command
        cmd = ['ngrok', 'http', str(port), '--region', region]
        
        if subdomain:
            cmd.extend(['--subdomain', subdomain])
        
        try:
            logger.info(f"🚀 Starting ngrok tunnel for port {port}...")
            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                                          stderr=subprocess.PIPE)
            
            # Wait for ngrok to start and get the URL
            for attempt in range(10):  # Try for 10 seconds
                time.sleep(1)
                url = self._get_tunnel_url()
                if url:
                    self.tunnel_url = url
                    logger.info(f"✅ Ngrok tunnel active: {url}")
                    return url
            
            logger.error("❌ Failed to get ngrok tunnel URL")
            self.stop_tunnel()
            return None
            
        except Exception as e:
            logger.error(f"❌ Failed to start ngrok tunnel: {e}")
            return None
    
    def _get_tunnel_url(self) -> Optional[str]:
        """Get the public URL from ngrok API"""
        try:
            response = requests.get(self.api_url, timeout=2)
            if response.status_code == 200:
                data = response.json()
                tunnels = data.get('tunnels', [])
                for tunnel in tunnels:
                    if tunnel.get('proto') == 'https':
                        return tunnel.get('public_url')
                    elif tunnel.get('proto') == 'http':
                        # Prefer HTTPS, but fallback to HTTP
                        return tunnel.get('public_url')
        except Exception:
            pass
        return None
    
    def stop_tunnel(self):
        """Stop the ngrok tunnel"""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
                logger.info("🛑 Ngrok tunnel stopped")
            except subprocess.TimeoutExpired:
                self.process.kill()
                logger.warning("⚠️  Ngrok process killed (didn't terminate gracefully)")
            except Exception as e:
                logger.error(f"❌ Error stopping ngrok: {e}")
            finally:
                self.process = None
                self.tunnel_url = None
    
    def get_tunnel_info(self) -> Dict[str, Any]:
        """Get detailed tunnel information"""
        if not self.tunnel_url:
            return {}
        
        try:
            response = requests.get(self.api_url, timeout=2)
            if response.status_code == 200:
                data = response.json()
                tunnels = data.get('tunnels', [])
                for tunnel in tunnels:
                    if tunnel.get('public_url') == self.tunnel_url:
                        return {
                            'public_url': tunnel.get('public_url'),
                            'proto': tunnel.get('proto'),
                            'config': tunnel.get('config', {}),
                            'metrics': tunnel.get('metrics', {})
                        }
        except Exception as e:
            logger.error(f"Error getting tunnel info: {e}")
        
        return {'public_url': self.tunnel_url}
    
    def is_tunnel_active(self) -> bool:
        """Check if tunnel is currently active"""
        return self.tunnel_url is not None and self.process is not None
    
    def print_tunnel_info(self):
        """Print user-friendly tunnel information"""
        if not self.tunnel_url:
            print("❌ No active ngrok tunnel")
            return
        
        info = self.get_tunnel_info()
        print("\n" + "="*60)
        print("🌐 NGROK TUNNEL ACTIVE")
        print("="*60)
        print(f"📡 Public URL: {self.tunnel_url}")
        print(f"🔒 Protocol: {info.get('proto', 'unknown').upper()}")
        print("💡 Share this URL to let others access your Face Swap Live server!")
        print("⚠️  Warning: Anyone with this URL can access your server")
        print("="*60)

# Global instance
_ngrok_manager = None

def get_ngrok_manager() -> NgrokManager:
    """Get the global ngrok manager instance"""
    global _ngrok_manager
    if _ngrok_manager is None:
        _ngrok_manager = NgrokManager()
    return _ngrok_manager