import requests
import json

class TestWebhookAPI:
    def __init__(self):
        self.base_url = "http://127.0.0.1:5000"
        self.webhook_url = f"{self.base_url}/api/webhook"
        self.server_url = "https://e.lambda-url.us-east-2.on.aws/api/webhook"
        self.balances_url = f"{self.base_url}/api/balances"
        
    def test_buy_webhook(self):
        """Test buying via webhook."""
        test_json = {
            "bot_id": "Gaussian",
            "ticker": "BTCUSDC",
            "action": "buy",
            "timestamp": "2025-06-01T12:00:00Z"
        }
        response = requests.post(self.webhook_url, json=test_json)
        if response.json()["status"] == "success":
            print("Buy Webhook processed successfully")
        else:
            print("Error processing Buy Webhook")
        
    def test_buy_webhook_server(self):
        """Test buying via webhook."""
        test_json = {
            "bot_id": "Gaussian",
            "ticker": "BTCUSDC",
            "action": "buy",
            "timestamp": "2025-06-01T12:00:00Z"
        }
        response = requests.post(self.server_url, json=test_json)
        print(json.dumps(response.json(), indent=4))
        print(response.status_code)
        if response.json()["status"] == "success":
            print("Buy Webhook processed successfully")
        else:
            print("Error processing Buy Webhook")
            
    def test_sell_webhook_server(self):
        """Test buying via webhook."""
        test_json = {
            "bot_id": "Gaussian",
            "ticker": "BTCUSDC",
            "action": "sell",
            "timestamp": "2025-06-01T12:00:00Z"
        }
        response = requests.post(self.server_url, json=test_json)
        print(json.dumps(response.json(), indent=4))
        print(response.status_code)
        if response.json()["status"] == "success":
            print("Buy Webhook processed successfully")
        else:
            print("Error processing Buy Webhook")
            
    def test_sell_webhook(self):
        """Test selling via webhook."""
        test_json = {
            "bot_id": "Gaussian",
            "ticker": "BTCUSDT",
            "action": "sell",
            "timestamp": "2025-06-01T12:00:00Z"
        }
        response = requests.post(self.webhook_url, json=test_json)
        print(response.json())
        if response.json()["status"] == "success":
            print("Sell Webhook processed successfully")
        else:
            print("Error processing Sell Webhook")

    def test_get_balances(self):
        """Test fetching account balances."""
        response = requests.get(self.balances_url)
        print(response.json()["status"])
        if response.json()["status"] == "success":
            print("Balances fetched successfully")
            print("Balances:", response.json())
        else:
            print("Error fetching balances", response.json())
            
if __name__ == "__main__":
    test_api = TestWebhookAPI()
    # test_api.test_buy_webhook()
    # test_api.test_buy_webhook_server()
    # test_api.test_sell_webhook_server()
    # test_api.test_sell_webhook()
    # test_api.test_get_balances()