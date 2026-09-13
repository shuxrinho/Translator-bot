"""
Main entry point for the Telegram Translation Bot.
Includes a simple HTTP server for health checks (similar to Java version).
"""
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from my_bot import MyBot


class HealthCheckHandler(BaseHTTPRequestHandler):
    """Simple HTTP handler for health check endpoint."""
    
    def do_GET(self):
        """Handle GET requests."""
        response = b"Bot is running!"
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(response)
        
    def log_message(self, format, *args):
        """Suppress default logging."""
        pass


def start_http_server(port: int):
    """Start HTTP server for health checks."""
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    print(f"Dummy server started on port {port}")
    server.serve_forever()


def main():
    """Main entry point."""
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 8080))
    
    # Start HTTP server in a separate thread
    server_thread = threading.Thread(target=start_http_server, args=(port,))
    server_thread.daemon = True
    server_thread.start()
    
    # Initialize and run the bot
    try:
        bot = MyBot()
        bot.run()
    except Exception as e:
        print(f"Error starting bot: {e}")
        raise


if __name__ == "__main__":
    main()
