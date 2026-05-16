"""
Local tracking server for email open tracking
Runs on PC to track email opens via tracking pixels
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
from tracking_hash import TrackingHashGenerator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TrackingHandler(BaseHTTPRequestHandler):
    """HTTP handler for tracking pixel requests"""
    
    def do_GET(self):
        """Handle GET request for tracking pixel"""
        try:
            # Parse URL
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)
            
            # Get hash from query parameter
            hash_value = params.get('mb', [None])[0] or params.get('hash', [None])[0]
            
            if hash_value:
                # Get client info
                ip_address = self.client_address[0]
                user_agent = self.headers.get('User-Agent', '')
                
                # Record the open
                result = TrackingHashGenerator.record_open(
                    hash_value=hash_value,
                    ip_address=ip_address,
                    user_agent=user_agent
                )
                
                if result['status'] == 'success':
                    logger.info(f"Email opened: {result['email_open'].email} (Hash: {hash_value[:10]}...)")
                else:
                    logger.warning(f"Failed to record open: {result.get('message', 'Unknown error')}")
            
            # Return 1x1 transparent PNG pixel
            self.send_response(200)
            self.send_header('Content-Type', 'image/png')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            self.end_headers()
            
            # 1x1 transparent PNG
            pixel = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xdb\x00\x00\x00\x00IEND\xaeB`\x82'
            self.wfile.write(pixel)
            
        except Exception as e:
            logger.error(f"Error handling tracking request: {str(e)}")
            self.send_response(500)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass

class TrackingServer:
    """Local tracking server for email opens"""
    
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.server = None
        self.thread = None
        self.running = False
    
    def start(self):
        """Start the tracking server"""
        if self.running:
            logger.info("Tracking server is already running")
            return True
        
        try:
            # Check if port is already in use (another instance might be running)
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((self.host, self.port))
            sock.close()
            
            if result == 0:
                # Port is in use - assume another instance is running
                logger.info(f"Port {self.port} is already in use. Tracking server appears to be running.")
                self.running = True  # Mark as running even though we didn't start it
                return True
            
            # Port is free, start the server
            self.server = HTTPServer((self.host, self.port), TrackingHandler)
            self.running = True
            
            def run_server():
                logger.info(f"Tracking server started on http://{self.host}:{self.port}")
                self.server.serve_forever()
            
            self.thread = threading.Thread(target=run_server, daemon=True)
            self.thread.start()
            
            logger.info(f"✓ Tracking server running at http://{self.host}:{self.port}/track.php")
            return True
        except OSError as e:
            error_msg = str(e).lower()
            if "address already in use" in error_msg or "only one usage of each socket address" in error_msg or "address already in use" in error_msg:
                # Port is in use - assume another instance is running
                logger.info(f"Port {self.port} is already in use. Tracking server appears to be running.")
                self.running = True
                return True
            else:
                logger.error(f"Failed to start tracking server: {str(e)}")
                self.running = False
                return False
        except Exception as e:
            logger.error(f"Failed to start tracking server: {str(e)}")
            self.running = False
            return False
    
    def stop(self):
        """Stop the tracking server"""
        if self.server and self.running:
            self.server.shutdown()
            self.running = False
            logger.info("Tracking server stopped")
    
    def get_tracking_url(self, hash_value: str) -> str:
        """Get tracking URL for a hash"""
        return f"http://{self.host}:{self.port}/track.php?mb={hash_value}"
    
    def is_running(self) -> bool:
        """Check if server is running"""
        return self.running

# Global tracking server instance
_tracking_server = None

def get_tracking_server(host='localhost', port=8080) -> TrackingServer:
    """Get or create tracking server instance"""
    global _tracking_server
    if _tracking_server is None:
        _tracking_server = TrackingServer(host, port)
    return _tracking_server

def start_tracking_server(host='localhost', port=8080) -> bool:
    """Start the global tracking server"""
    server = get_tracking_server(host, port)
    return server.start()

def stop_tracking_server():
    """Stop the global tracking server"""
    global _tracking_server
    if _tracking_server:
        _tracking_server.stop()

if __name__ == "__main__":
    # Run server standalone
    server = TrackingServer('localhost', 8080)
    print("Starting tracking server...")
    print(f"Server will run at: http://localhost:8080/track.php?mb=HASH")
    print("Press Ctrl+C to stop")
    
    try:
        server.start()
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping server...")
        server.stop()

