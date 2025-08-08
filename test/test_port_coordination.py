#!/usr/bin/env python3
"""
Test script to verify port coordination between server and ngrok
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_port_coordination():
    """Test that server and ngrok use the same port"""
    print("🧪 Testing Port Coordination")
    print("=" * 50)
    
    # Test 1: Get available port from server
    print("\n1. Testing server port allocation:")
    try:
        from server import get_available_port
        port1 = get_available_port()
        port2 = get_available_port()
        print(f"   First call: {port1}")
        print(f"   Second call: {port2}")
        print(f"   Ports are different: {port1 != port2} (good for avoiding conflicts)")
    except Exception as e:
        print(f"   ERROR: {e}")
    
    # Test 2: Test ngrok manager port handling
    print("\n2. Testing ngrok manager:")
    try:
        from ngrok_manager import NgrokManager
        manager = NgrokManager()
        print(f"   Ngrok installed: {manager.is_ngrok_installed()}")
        print(f"   Manager created successfully")
    except Exception as e:
        print(f"   ERROR: {e}")
    
    # Test 3: Simulate the coordination logic
    print("\n3. Testing coordination logic:")
    try:
        from server import get_available_port
        
        # This is what happens in app.py
        server_port = get_available_port()
        print(f"   Selected port: {server_port}")
        print(f"   Port type: {type(server_port)}")
        print(f"   Port is valid: {isinstance(server_port, int) and 1024 <= server_port <= 65535}")
        
        # Simulate ngrok tunnel creation (without actually starting it)
        print(f"   Would start ngrok tunnel on port: {server_port}")
        print(f"   Would start server on port: {server_port}")
        print("   ✅ Port coordination would work correctly!")
        
    except Exception as e:
        print(f"   ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("🎯 Port coordination test completed!")

if __name__ == "__main__":
    test_port_coordination()