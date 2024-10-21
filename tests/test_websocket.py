import unittest
import json
import logging
import pytest
from src.websocket_util import open_connection, close_connection, send_request

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("logs/test_log.log"),  
                        logging.StreamHandler()                
                    ])
class TestWebSocketDerivAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open('configs/config.json') as config_file:
            cls.config = json.load(config_file)

    def setUp(self):
        
        self.ws = open_connection(self.config['websocket_url'])
        logging.info("WebSocket connection opened.")

    def tearDown(self):
        close_connection(self.ws)
        logging.info("WebSocket connection closed.")

    def test_TC001_UT_Open_Connection(self):
        """Test opening a WebSocket connection."""
        self.assertIsNotNone(self.ws, "WebSocket handshake failed!")
        self.assertTrue(self.ws.connected, "WebSocket should be connected.")
        logging.info("SUCCESS - test_TC001_UT_Open_Connection")

    def test_TC002_UT_Close_Connection(self):
        """Test closing the WebSocket connection."""
        close_connection(self.ws)
        self.assertFalse(self.ws.connected, "WebSocket should be closed.")
        logging.info("SUCCESS - test_TC002_UT_Close_Connection")

    def test_TC003_UT_Send_Valid_Request(self):
        """Test sending a valid request through WebSocket."""
        try:
            request = {"method": "subscribe", "params": {"channel": "states_list"}}
            logging.info(f"Sending request: {request}")
            response = send_request(self.ws, request)
            logging.info(f"Received response: {response}")
            self.assertIsNotNone(response, "Response should not be None for a valid request.")
            self.assertIn("echo_req", response, "Response should contain 'echo_req'.")
            self.assertIn("error", response, "Response should contain 'error'.")
            self.assertIn("code", response["error"], "Error response should contain 'code'.")
            self.assertIn("message", response["error"], "Error response should contain 'message'.")
            logging.info("SUCCESS - test_TC003_UT_Send_Valid_Request")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            self.fail(f"Unexpected error: {e}")

    def test_TC004_UT_Send_Invalid_Request(self):
        """Test sending an invalid request and handling the error."""
        try:
            invalid_request = {"method": "invalid", "params": {}}
            logging.info(f"Sending invalid request: {invalid_request}")
            response = send_request(self.ws, invalid_request)
            logging.info(f"Received response: {response}")
            self.assertIsNotNone(response, "Response should not be None for an invalid request.")
            self.assertIn("echo_req", response, "Response should contain 'echo_req'.")
            self.assertIn("error", response, "Response should contain 'error'.")
            self.assertIn("code", response["error"], "Error response should contain 'code'.")
            self.assertIn("message", response["error"], "Error response should contain 'message'.")
            logging.info("SUCCESS - test_TC004_UT_Send_Invalid_Request")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            self.fail(f"Unexpected error: {e}")

    def test_TC005_UT_Connection_Timeout(self):
        """Test handling of connection timeout."""
        try:
            logging.info("Attempting to open WebSocket connection with invalid URL.")
            websocket = open_connection("ws://invalid-url") 
            self.assertIsNone(websocket, "WebSocket connection should fail for an invalid URL.")
            logging.info("SUCCESS - test_TC005_UT_Connection_Timeout")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            self.fail(f"Unexpected error: {e}")

if __name__ == "__main__":
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='report'))

