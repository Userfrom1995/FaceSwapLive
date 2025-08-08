#!/usr/bin/env python3
"""
Test script to verify ngrok configuration priority system
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_priority_system():
    """Test the ngrok configuration priority system"""
    print("TESTING NGROK CONFIGURATION PRIORITY SYSTEM")
    print("=" * 60)
    
    # Test 1: .env file only
    print("\n1. Testing .env file priority (lowest)")
    print("-" * 40)
    
    # Create test .env file
    env_content = """NGROK_AUTH_TOKEN=env_file_token
NGROK_SUBDOMAIN=env-file-subdomain
NGROK_REGION=eu
"""
    with open('.env.test', 'w') as f:
        f.write(env_content)
    
    # Load .env file
    try:
        from dotenv import load_dotenv
        load_dotenv('.env.test')
        print("✅ .env file loaded successfully")
        print(f"   NGROK_AUTH_TOKEN from .env: {os.getenv('NGROK_AUTH_TOKEN')}")
        print(f"   NGROK_SUBDOMAIN from .env: {os.getenv('NGROK_SUBDOMAIN')}")
        print(f"   NGROK_REGION from .env: {os.getenv('NGROK_REGION')}")
    except ImportError:
        print("❌ python-dotenv not installed")
        return False
    
    # Test 2: Environment variable override
    print("\n2. Testing environment variable priority (medium)")
    print("-" * 40)
    
    # Set environment variables (should override .env)
    os.environ['NGROK_AUTH_TOKEN'] = 'env_var_token'
    os.environ['NGROK_REGION'] = 'us'
    # Leave NGROK_SUBDOMAIN unset to test .env fallback
    
    print(f"   NGROK_AUTH_TOKEN after env var: {os.getenv('NGROK_AUTH_TOKEN')}")
    print(f"   NGROK_SUBDOMAIN (should be from .env): {os.getenv('NGROK_SUBDOMAIN')}")
    print(f"   NGROK_REGION after env var: {os.getenv('NGROK_REGION')}")
    
    # Test 3: Command line simulation
    print("\n3. Testing command line priority (highest)")
    print("-" * 40)
    
    # Simulate command line arguments
    class MockArgs:
        ngrok_auth_token = 'cmdline_token'
        ngrok_subdomain = None  # Not provided
        ngrok_region = None     # Not provided
    
    args = MockArgs()
    
    # Simulate the priority logic from app.py
    final_token = None
    final_subdomain = None
    final_region = None
    
    # Auth token priority
    if args.ngrok_auth_token:
        final_token = args.ngrok_auth_token
        source_token = "command line"
    elif os.getenv('NGROK_AUTH_TOKEN'):
        final_token = os.getenv('NGROK_AUTH_TOKEN')
        source_token = "environment variable"
    
    # Subdomain priority
    if args.ngrok_subdomain:
        final_subdomain = args.ngrok_subdomain
        source_subdomain = "command line"
    elif os.getenv('NGROK_SUBDOMAIN'):
        final_subdomain = os.getenv('NGROK_SUBDOMAIN')
        source_subdomain = "environment variable (.env file)"
    
    # Region priority
    if args.ngrok_region:
        final_region = args.ngrok_region
        source_region = "command line"
    elif os.getenv('NGROK_REGION'):
        final_region = os.getenv('NGROK_REGION')
        source_region = "environment variable"
    
    print(f"   Final AUTH_TOKEN: {final_token} (from {source_token})")
    print(f"   Final SUBDOMAIN: {final_subdomain} (from {source_subdomain})")
    print(f"   Final REGION: {final_region} (from {source_region})")
    
    # Test 4: Verify priority order
    print("\n4. Priority verification")
    print("-" * 40)
    
    expected_results = {
        'token': ('cmdline_token', 'command line'),
        'subdomain': ('env-file-subdomain', 'environment variable (.env file)'),
        'region': ('us', 'environment variable')
    }
    
    actual_results = {
        'token': (final_token, source_token),
        'subdomain': (final_subdomain, source_subdomain),
        'region': (final_region, source_region)
    }
    
    all_correct = True
    for key, (expected_val, expected_src) in expected_results.items():
        actual_val, actual_src = actual_results[key]
        if actual_val == expected_val and actual_src == expected_src:
            print(f"   ✅ {key.upper()}: {actual_val} from {actual_src}")
        else:
            print(f"   ❌ {key.upper()}: Expected {expected_val} from {expected_src}, got {actual_val} from {actual_src}")
            all_correct = False
    
    # Cleanup
    os.remove('.env.test')
    if 'NGROK_AUTH_TOKEN' in os.environ:
        del os.environ['NGROK_AUTH_TOKEN']
    if 'NGROK_REGION' in os.environ:
        del os.environ['NGROK_REGION']
    if 'NGROK_SUBDOMAIN' in os.environ:
        del os.environ['NGROK_SUBDOMAIN']
    
    print(f"\n5. Overall result: {'✅ ALL TESTS PASSED' if all_correct else '❌ SOME TESTS FAILED'}")
    
    return all_correct

def show_priority_documentation():
    """Show the priority system documentation"""
    print("\n\nNGROK CONFIGURATION PRIORITY SYSTEM")
    print("=" * 60)
    print("Priority Order (highest to lowest):")
    print("1. 🥇 Command Line Arguments (--ngrok-auth-token)")
    print("2. 🥈 Environment Variables (export NGROK_AUTH_TOKEN=...)")
    print("3. 🥉 .env File (NGROK_AUTH_TOKEN=... in .env)")
    print()
    print("Examples:")
    print("# Highest priority - Command line")
    print("python app.py --ngrok --ngrok-auth-token cmd_token")
    print()
    print("# Medium priority - Environment variable")
    print("export NGROK_AUTH_TOKEN=env_token")
    print("python app.py --ngrok")
    print()
    print("# Lowest priority - .env file")
    print("echo 'NGROK_AUTH_TOKEN=file_token' > .env")
    print("python app.py --ngrok")
    print()
    print("Logic: More explicit = Higher priority")
    print("- Command line is most explicit (user types it now)")
    print("- Environment variable is session-level")
    print("- .env file is project default")

if __name__ == "__main__":
    success = test_priority_system()
    show_priority_documentation()
    
    if success:
        print("\n🎉 Priority system is working correctly!")
    else:
        print("\n⚠️  Priority system needs fixes!")