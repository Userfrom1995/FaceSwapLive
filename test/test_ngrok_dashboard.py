#!/usr/bin/env python3
"""
Test script to verify ngrok dashboard port configuration
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_dashboard_config():
    """Test ngrok dashboard configuration"""
    print("🧪 Testing Ngrok Dashboard Configuration")
    print("=" * 50)
    
    # Test 1: Default configuration
    print("\n1. Testing default configuration:")
    try:
        from config import config
        print(f"   Default dashboard port: {config.ngrok.DASHBOARD_PORT}")
        print(f"   Expected: 4040")
        print(f"   ✅ Correct: {config.ngrok.DASHBOARD_PORT == 4040}")
    except Exception as e:
        print(f"   ERROR: {e}")
    
    # Test 2: NgrokManager initialization
    print("\n2. Testing NgrokManager initialization:")
    try:
        from ngrok_manager import NgrokManager
        
        # Test with default port
        manager1 = NgrokManager()
        print(f"   Default manager dashboard port: {manager1.dashboard_port}")
        print(f"   Dashboard URL: {manager1.dashboard_url}")
        
        # Test with custom port
        manager2 = NgrokManager(dashboard_port=4041)
        print(f"   Custom manager dashboard port: {manager2.dashboard_port}")
        print(f"   Custom dashboard URL: {manager2.dashboard_url}")
        
        print("   ✅ NgrokManager initialization works")
    except Exception as e:
        print(f"   ERROR: {e}")
    
    # Test 3: API URL construction
    print("\n3. Testing API URL construction:")
    try:
        from ngrok_manager import NgrokManager
        
        manager = NgrokManager(dashboard_port=4040)
        expected_api = "http://localhost:4040/api/tunnels"
        expected_dashboard = "http://localhost:4040"
        
        print(f"   API URL: {manager.api_url}")
        print(f"   Expected: {expected_api}")
        print(f"   ✅ API URL correct: {manager.api_url == expected_api}")
        
        print(f"   Dashboard URL: {manager.dashboard_url}")
        print(f"   Expected: {expected_dashboard}")
        print(f"   ✅ Dashboard URL correct: {manager.dashboard_url == expected_dashboard}")
        
    except Exception as e:
        print(f"   ERROR: {e}")
    
    # Test 4: Environment variable override
    print("\n4. Testing environment variable override:")
    try:
        import os
        
        # Set environment variable
        os.environ['NGROK_DASHBOARD_PORT'] = '4041'
        
        # Reload config
        from config import load_environment_overrides, config
        load_environment_overrides()
        
        print(f"   Dashboard port after env override: {config.ngrok.DASHBOARD_PORT}")
        print(f"   Expected: 4041")
        print(f"   ✅ Environment override works: {config.ngrok.DASHBOARD_PORT == 4041}")
        
        # Clean up
        del os.environ['NGROK_DASHBOARD_PORT']
        
    except Exception as e:
        print(f"   ERROR: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Dashboard configuration test completed!")

if __name__ == "__main__":
    test_dashboard_config()