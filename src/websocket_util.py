import logging
import json  # Import the json module
from websocket import create_connection, WebSocketConnectionClosedException

def open_connection(url):
    """Establish a WebSocket connection."""
    try:
        ws = create_connection(url, timeout=5)
        logging.info("WebSocket connection established.")
        return ws
    except Exception as e:
        logging.error(f"Failed to establish WebSocket connection: {e}")
        return None

def close_connection(ws):
    """Close the WebSocket connection."""
    if ws:
        try:
            ws.close()
            logging.info("WebSocket connection closed.")
        except Exception as e:
            logging.error(f"Error closing WebSocket connection: {e}")

def send_request(ws, request):
    """Send a request to the WebSocket and return the response."""
    if ws:
        # Check if the request is a dictionary and convert to JSON
        if isinstance(request, dict):
            request_json = json.dumps(request)
        else:
            logging.error("Invalid request format. Must be a dictionary.")
            return None

        try:
            # Ensure the WebSocket connection is still open
            if ws.sock and ws.sock.fileno() != -1:
                ws.send(request_json)
                logging.info(f"Request sent: {request_json}")
                
                # Receive and parse the response
                response = ws.recv()
                logging.info(f"Response received: {response}")
                return json.loads(response)
            else:
                logging.error("WebSocket connection is closed.")
                return None
        except WebSocketConnectionClosedException:
            logging.error("WebSocket connection was closed unexpectedly.")
            return None
        except Exception as e:
            logging.error(f"Failed to send request: {e}")
            return None
    else:
        logging.error("WebSocket connection not established.")
        return None