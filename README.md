# FlaskAWS - Coinbase Trading Bot API

## Description

This project is a FastAPI application designed to interact with the Coinbase API for fetching wallet balances and executing trades based on webhook signals. It provides a simple web interface to view balances and an API endpoint to receive trading signals from external sources.

## Features

-   **Wallet Balance Display**: Fetches and displays wallet balances for various cryptocurrencies from Coinbase.
-   **Trading via Webhooks**: Accepts trading signals via webhooks to automatically execute buy or sell orders.
-   **API Endpoints**: Provides API endpoints for retrieving balances and processing webhooks.
-   **Logging**: Implements detailed logging for debugging and monitoring.

## Prerequisites

-   Python 3.8+
-   Coinbase API Key and Secret
-   `pip` package installer

## Installation

1.  **Clone the repository:**

    ```bash
    git clone [repository_url]
    cd FlaskAWS
    ```

2.  **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Linux/Mac
    venv\Scripts\activate.bat  # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set environment variables:**

    Set your Coinbase API key and secret as environment variables:

    ```bash
    export COINBASE_API_KEY="your_coinbase_api_key"
    export COINBASE_API_SECRET="your_coinbase_api_secret"
    ```

    Or, on Windows:

    ```bash
    set COINBASE_API_KEY="your_coinbase_api_key"
    set COINBASE_API_SECRET="your_coinbase_api_secret"
    ```

## Usage

1.  **Run the application:**

    ```bash
    python app.py
    ```

    Or, if deploying with Mangum:

    ```bash
    mangum app.handler
    ```

2.  **Access the web interface:**

    Open your web browser and go to `http://localhost:8000` to view wallet balances.

## API Endpoints

### 1. Get Wallet Balances

-   **Endpoint:** `/api/balances`
-   **Method:** `GET`
-   **Response:**

    ```json
    {
        "status": "success",
        "balances": [
            {"currency": "CAD", "balance": "100.00"},
            {"currency": "USDC", "balance": "50.00"},
            {"currency": "BTC", "balance": "0.001"}
        ]
    }
    ```

### 2. Process Trading Signals (Webhook)

-   **Endpoint:** `/api/webhook`
-   **Method:** `POST`
-   **Request Body:**

    ```json
    {
        "bot_id": "trading_bot_name",
        "ticker": "BTCUSDC",
        "action": "buy",  // or "sell"
        "timestamp": "2023-06-01T12:00:00Z"
    }
    ```

-   **Response:**

    ```json
    {
        "status": "success",
        "message": "Processed buy order for BTCUSDC"
    }
    ```

## Error Handling

The application provides error responses in JSON format for API endpoints. Errors are also logged for debugging purposes.

## Dependencies

-   fastapi
-   Jinja2
-   coinbase
-   mangum
-   uvicorn

## Configuration

-   **Environment Variables**:
    -   `COINBASE_API_KEY`: Your Coinbase API key.
    -   `COINBASE_API_SECRET`: Your Coinbase API secret.

## Logging

The application uses the `logging` module to log important events, errors, and debugging information. Logs are configured to output to the console.

## Deployment

This application can be deployed to AWS Lambda using Mangum. Ensure that the necessary AWS resources are configured, including API Gateway and IAM roles.

## License

[MIT License](LICENSE)