"""
Face Swap Live - Application Entry Point

This is the main entry point for the Face Swap Live application.
Run this file to start the server with all optimizations and proper cleanup.

Usage:
    python app.py [--host HOST] [--port PORT] [--debug]

Features:
- Automatic model initialization
- Smart port management
- Graceful shutdown handling
- Performance monitoring
- Single-user optimization
"""

import argparse
import sys
import os
import logging
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config import config
from server import start_server
from pipeline import initialize_pipeline
# from server_fast import start_fast_server
# from pipeline_fast import initialize_fast_pipeline


# Configure logging
logging.basicConfig(
    level=getattr(logging, config.logging.LOG_LEVEL),
    format=config.logging.LOG_FORMAT,
    datefmt=config.logging.DATE_FORMAT
)
logger = logging.getLogger(__name__)

def print_banner():
    """Print application banner with information"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                     FACE SWAP LIVE                          ║
    ║                Real-time Face Swapping Server               ║
    ╠══════════════════════════════════════════════════════════════╣
    ║  🚀 High Performance  │  🎯 Single User Optimized          ║
    ║  🎮 GPU Accelerated   │  🌐 Web-based Interface            ║
    ║  📹 Real-time Video   │  🔧 Professional Grade             ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_requirements():
    """
    Check if all requirements are met before starting the server.
    
    Returns:
        bool: True if all requirements are satisfied
    """
    logger.info("Checking system requirements...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        logger.error("Python 3.8 or higher is required")
        return False
    
    # Check if models directory exists
    models_dir = config.models.MODELS_DIR
    if not models_dir.exists():
        logger.info(f"Creating models directory: {models_dir}")
        models_dir.mkdir(parents=True, exist_ok=True)
    
    # Check for required model files
    required_models = config.models.FACE_SWAPPER_MODELS
    available_models = []
    
    for model_name in required_models:
        model_path = models_dir / model_name
        if model_path.exists():
            available_models.append(model_name)
            logger.info(f"Found model: {model_name}")
    
    if not available_models:
        logger.warning("No face swap models found in models directory")
        logger.info("The application will attempt to download models automatically")
        logger.info("Or you can manually download models to: " + str(models_dir))
        
        # List download URLs for manual download
        logger.info("\nModel download URLs:")
        for model_name, url in config.models.MODEL_URLS.items():
            logger.info(f"  {model_name}: {url}")
    
    # Check templates directory
    templates_dir = project_root / "templates"
    if not templates_dir.exists():
        logger.error(f"Templates directory not found: {templates_dir}")
        return False
    
    # Check if index.html exists
    index_template = templates_dir / "index.html"
    if not index_template.exists():
        logger.error(f"Main template not found: {index_template}")
        return False
    
    logger.info("System requirements check completed")
    return True

def setup_environment():
    """Setup environment variables and configurations"""
    
    # Set environment variables for optimal performance
    os.environ['OMP_NUM_THREADS'] = '1'  # Prevent OpenMP conflicts
    os.environ['MKL_NUM_THREADS'] = '1'  # Intel MKL optimization
    
    # CUDA optimizations if available
    try:
        import torch
        if torch.cuda.is_available():
            # Set CUDA device if not already set
            if 'CUDA_VISIBLE_DEVICES' not in os.environ:
                os.environ['CUDA_VISIBLE_DEVICES'] = '0'
            
            logger.info(f"CUDA available: {torch.cuda.get_device_name(0)}")
            logger.info(f"CUDA memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
        else:
            logger.info("CUDA not available, using CPU processing")
    except ImportError:
        logger.warning("PyTorch not available, some optimizations disabled")

def parse_arguments():
    """
    Parse command line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Face Swap Live - Real-time Face Swapping Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python app.py                              # Start with default settings
  python app.py --port 8080                  # Start on specific port
  python app.py --host 0.0.0.0               # Listen on all interfaces
  python app.py --debug                      # Enable debug mode
  python app.py --ngrok                      # Enable ngrok tunnel (public access)
  python app.py --ngrok --ngrok-auth-token YOUR_TOKEN  # Ngrok with auth token
  python app.py --ngrok --ngrok-subdomain myapp       # Custom subdomain (paid plan)
  
Ngrok Setup:
  1. Sign up at https://ngrok.com and get your auth token
  2. Use --ngrok-auth-token YOUR_TOKEN or set NGROK_AUTH_TOKEN environment variable
  3. For custom subdomains, upgrade to a paid plan
        """
    )
    
    parser.add_argument(
        '--host',
        type=str,
        default=config.server.HOST,
        help=f'Server host address (default: {config.server.HOST})'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=None,
        help='Server port number (default: auto-detect)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode'
    )
    
    parser.add_argument(
        '--no-gpu',
        action='store_true',
        help='Disable GPU acceleration'
    )
    
    parser.add_argument(
        '--models-dir',
        type=str,
        default=str(config.models.MODELS_DIR),
        help=f'Models directory path (default: {config.models.MODELS_DIR})'
    )
    
    # Ngrok arguments
    parser.add_argument(
        '--ngrok',
        action='store_true',
        help='Enable ngrok tunnel for public access'
    )
    
    parser.add_argument(
        '--ngrok-auth-token',
        type=str,
        help='Ngrok authentication token'
    )
    
    parser.add_argument(
        '--ngrok-subdomain',
        type=str,
        help='Custom ngrok subdomain (requires paid plan)'
    )
    
    parser.add_argument(
        '--ngrok-region',
        type=str,
        default=config.ngrok.REGION,
        choices=['us', 'eu', 'ap', 'au', 'sa', 'jp', 'in'],
        help=f'Ngrok region (default: {config.ngrok.REGION})'
    )
    
    return parser.parse_args()

def apply_arguments(args):
    """
    Apply command line arguments to configuration.
    
    Args:
        args: Parsed command line arguments
    """
    if args.debug:
        config.development.DEBUG_MODE = True
        config.logging.LOG_LEVEL = "DEBUG"
        logger.setLevel(logging.DEBUG)
        logger.info("Debug mode enabled")
    
    if args.no_gpu:
        config.models.USE_GPU = False
        logger.info("GPU acceleration disabled")
    
    if args.models_dir:
        config.models.MODELS_DIR = Path(args.models_dir)
        logger.info(f"Models directory set to: {config.models.MODELS_DIR}")
    
    # Apply ngrok arguments
    if args.ngrok:
        config.ngrok.ENABLE_NGROK = True
        logger.info("Ngrok tunnel enabled")
    
    if args.ngrok_auth_token:
        config.ngrok.AUTH_TOKEN = args.ngrok_auth_token
        logger.info("Ngrok auth token provided")
    
    if args.ngrok_subdomain:
        config.ngrok.SUBDOMAIN = args.ngrok_subdomain
        logger.info(f"Ngrok subdomain set to: {args.ngrok_subdomain}")
    
    if args.ngrok_region:
        config.ngrok.REGION = args.ngrok_region
        logger.info(f"Ngrok region set to: {args.ngrok_region}")

def main():
    """Main application entry point"""
    
    # Print banner
    print_banner()
    
    # Parse command line arguments
    args = parse_arguments()
    apply_arguments(args)
    
    # Setup environment
    setup_environment()
    
    # Check requirements
    if not check_requirements():
        logger.error("Requirements check failed. Please fix the issues and try again.")
        sys.exit(1)
    
    # Initialize pipeline
    logger.info("Initializing face swap pipeline...")
    if not initialize_pipeline():
        logger.error("Failed to initialize face swap pipeline")
        logger.error("Please check that required models are available")
        sys.exit(1)
    
    logger.info("Pipeline initialized successfully")
    
    # Start server
    ngrok_manager = None
    try:
        logger.info("Starting Face Swap Live server...")
        
        # Determine the port that will be used by the server
        if args.port:
            server_port = args.port
            logger.info(f"Using specified port: {server_port}")
        else:
            # Use the server's port finding logic to get an available port
            from server import get_available_port
            server_port = get_available_port()
            logger.info(f"Found available port: {server_port}")
        
        # Start ngrok tunnel if enabled (now we know the exact port)
        if config.ngrok.ENABLE_NGROK:
            from ngrok_manager import NgrokManager
            ngrok_manager = NgrokManager(dashboard_port=config.ngrok.DASHBOARD_PORT)
            
            logger.info(f"Starting ngrok tunnel for port {server_port}...")
            
            # Start tunnel with the determined port
            tunnel_url = ngrok_manager.start_tunnel(
                port=server_port,
                auth_token=config.ngrok.AUTH_TOKEN,
                subdomain=config.ngrok.SUBDOMAIN,
                region=config.ngrok.REGION
            )
            
            if tunnel_url:
                # Verify the tunnel is correctly configured
                if ngrok_manager.verify_tunnel(server_port):
                    tunnel_details = ngrok_manager.get_tunnel_details()
                    ngrok_manager.print_tunnel_info()
                    logger.info(f"Ngrok tunnel verified - Server will start on port {server_port}")
                    logger.info(f"Tunnel: {tunnel_details.get('public_url')} -> {tunnel_details.get('local_addr', f'localhost:{server_port}')}")
                else:
                    logger.warning("Tunnel verification failed, but continuing anyway")
                    ngrok_manager.print_tunnel_info()
                
                # Open browser if configured
                if config.ngrok.AUTO_OPEN_BROWSER:
                    try:
                        import webbrowser
                        webbrowser.open(tunnel_url)
                        logger.info("Opened tunnel URL in browser")
                    except Exception as e:
                        logger.warning(f"Could not open browser: {e}")
            else:
                logger.warning("Ngrok tunnel failed to start, continuing with local server only")
                logger.info(f"Server will be available locally at: http://localhost:{server_port}")
        
        # Start the actual server with the determined port
        success = start_server(host=args.host, port=server_port)
        
        if not success:
            logger.error("Failed to start server")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("Server interrupted by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)
    finally:
        # Clean up ngrok tunnel
        if ngrok_manager and ngrok_manager.is_tunnel_active():
            ngrok_manager.stop_tunnel()
        logger.info("Face Swap Live server shutdown complete")

if __name__ == "__main__":
    main()