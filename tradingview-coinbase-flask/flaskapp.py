import uuid
import json
import logging
import os
from flask import Flask, request, jsonify, render_template
from coinbase.rest import RESTClient
from mangum import Mangum

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
handler = Mangum(app)

# Load Coinbase API credentials from environment variables
def load_api_keys():
    api_key = os.environ.get('COINBASE_API_KEY')
    api_secret = os.environ.get('COINBASE_API_SECRET')
    if not api_key or not api_secret:
        raise ValueError("Coinbase API key and secret must be set in environment variables.")
    return api_key, api_secret

COINBASE_API_KEY, COINBASE_API_SECRET = load_api_keys()

# Initialize Coinbase client
def get_coinbase_client():
    try:
        client = RESTClient(
            api_key=COINBASE_API_KEY,
            api_secret=COINBASE_API_SECRET
        )
        logger.info("Coinbase client initialized successfully.")
        return client
    except Exception as e:
        logger.error(f"Error initializing Coinbase client: {e}")
        return None  # Or raise an exception

# API routes
@app.route('/')
def home():
    """Landing page that displays wallet balances"""
    try:
        # Get balances from Coinbase
        balances = get_account_balances()
        return render_template('index.html', balances=balances)
    except Exception as e:
        logger.error(f"Error fetching balances: {str(e)}")
        # Return template with empty balances if there's an error
        return render_template('index.html',  balances=[{'currency': 'CAD', 'balance': '***'}, {'currency': 'USDC', 'balance': '***'}, {'currency': 'BTC', 'balance': '***'}])

@app.route('/api/balances')
def api_balances():
    """API endpoint to get wallet balances"""
    try:
        balances = get_account_balances()
        return jsonify({
            "status": "success",
            "balances": balances
        })
    except Exception as e:
        logger.error(f"Error fetching balances: {str(e)}")
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/api/webhook', methods=['POST'])
def webhook():
    """
    Process incoming webhook requests with trading signals.
    Expected JSON format:
    {
        "bot_id": "trading_bot_name",
        "ticker": "BTCUSDC",
        "action": "buy", or "sell"
        "timestamp": "2023-06-01T12:00:00Z"
    }
    """
    # Get the JSON payload from the request
    payload = request.json
    # Log the received payload with an indent of 2 spaces
    logger.info(f"Received webhook payload:\n{json.dumps(payload, indent=2)}")
    
    # Extract ticker and action from the payload
    ticker = payload.get('ticker')
    action = payload.get('action')
    
    logger.info(f"Processing trade: {action} {ticker}")
    
    # Execute the trade based on the action
    if action.lower() == 'buy':
        execute_order(ticker, 'buy')
    elif action.lower() == 'sell':
        execute_order(ticker, 'sell')
    
    return jsonify({"status": "success", "message": f"Processed {action} order for {ticker}"}), 200

# Helper functions
def get_account_balances():
    """Get account balances from Coinbase"""
    coinbase_client = get_coinbase_client()
    accounts_response = coinbase_client.get_accounts()
    
    # Initialize balances with zeros
    balances = []
    
    # Access the accounts list directly from the response
    if hasattr(accounts_response, 'accounts'):
        for account in accounts_response.accounts:
            currency = account.currency
            balance = account.available_balance["value"]
            balances.append({'currency': currency, 'balance': balance})
    return balances

def get_available_balances(product_id):
    """Retrieve available balances for both base and quote currencies of the given product ID."""
    try:
        # Get account balances for all currencies
        accounts = get_account_balances()
        
        # Split product ID into base and quote currencies
        base_currency, quote_currency = product_id.split('-')
        
        # Initialize balances
        base_balance = 0.0
        quote_balance = 0.0
        
        # Get balances for both currencies
        for account in accounts:
            if account['currency'] == base_currency:
                base_balance = float(account['balance'])
            elif account['currency'] == quote_currency:
                quote_balance = float(account['balance'])
        
        return {
            'base': base_balance,
            'quote': quote_balance
        }
    except Exception as e:
        print(f"Error getting available balances: {e}")
        return {
            'base': 0.0,
            'quote': 0.0
        }

def get_product_id(ticker):
    """Get product ID from ticker symbol"""
    # List of known quote currencies, ordered by length descending to prioritize longer matches
    known_quotes = ["USDC", "USD", "USDT", "JPY"]

    # Convert ticker to uppercase for consistent processing
    ticker_upper = ticker.upper()
    
    # Iterate through known quotes to find the longest matching suffix
    for quote in sorted(known_quotes, key=lambda x: len(x), reverse=True):
        if ticker_upper.endswith(quote):
            base = ticker_upper[:-len(quote)]
            return f"{base}-{quote}"
    
    # If no known quote found, assume it's a single currency and append "-USD"
    return f"{ticker_upper}-USD"

def format_balance(value, decimals, slippage=0.0001):
    """Format a float value to a specified number of decimal places with slippage."""
    adjusted_value = value * (1 - slippage)
    value_str = f"{adjusted_value:.{decimals+1}f}"  # Format to one extra decimal place
    return value_str[:value_str.index('.') + decimals + 1]

def execute_order(ticker, side):
    """Execute an order for the specified ticker and side (buy/sell)."""
    logger.info(f"Executing {side.upper()} order for {ticker}")
    
    # Get product ID
    product_id = get_product_id(ticker)
    print("-------------Product ID:", product_id)
    
    # Get available balance
    balances = get_available_balances(product_id)
    available_balance = float(balances['quote' if side == 'buy' else 'base'])
    print("******Available balance:", balances)
    if side == 'buy':
        if available_balance > 1:
            order_configuration = {
                "market_market_ioc": {
                    "quote_size": format_balance(available_balance, 1)
                }
            }
        else:
            logger.info(f"Insufficient balance to execute buy order for {product_id.split('-')[1]}")
            return
    else:
        if available_balance > 0:
            order_configuration = {
                "market_market_ioc": {
                    "base_size": format_balance(available_balance, 8)
                }
            }
        else:
            logger.info(f"No {product_id.split('-')[0]} available to sell")
            return
    
    # Execute the order
    response = get_coinbase_client().create_order(
        product_id=product_id,
        side=side.upper(),
        order_configuration=order_configuration,
        client_order_id=str(uuid.uuid4().hex)
    )
    
    # Convert response to a dictionary for pretty printing
    response_dict = response.__dict__ if hasattr(response, '__dict__') else response
    logger.info(f"{side.capitalize()} order created:\n{json.dumps(response_dict, indent=2)}")