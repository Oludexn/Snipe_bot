import os
import telebot
from flask import Flask, request
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardButton
from nacl.signing import SigningKey
import requests

# Fetch API Token from environment variable
API_TOKEN = os.getenv("API_KEY")

# Ensure API_TOKEN is provided
if not API_TOKEN:
    raise ValueError("API_KEY environment variable is missing.")

# Initialize bot with API token
bot = telebot.TeleBot(API_TOKEN)

# Flask app setup for webhook
app = Flask(__name__)

# Solana RPC endpoint for checking balances
SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com"

wallets = {}

# Convert private key to public key
def get_public_key_from_private_key(private_key):
    key_bytes = bytes(map(int, private_key.split()))
    signing_key = SigningKey(key_bytes)
    return signing_key.verify_key.encode().hex()

# Verify private key and return balance and tokens
def verify_private_key(private_key):
    try:
        public_key = get_public_key_from_private_key(private_key)
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getBalance",
            "params": [public_key]
        }
        response = requests.post(SOLANA_RPC_URL, json=payload)
        result = response.json()
        
        if "result" in result and "value" in result["result"]:
            balance = result["result"]["value"] / 1e9  # Convert lamports to SOL
            return f"Private key verified successfully! Balance: {balance} SOL"
        else:
            return "Verification failed. No account balance found."

    except Exception as e:
        return f"Invalid private key format or error: {str(e)}"

# Webhook handler for incoming updates from Telegram
@app.route(f'/{API_TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data(as_text=True)
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

# Example save_wallet function
def save_wallet(user_id, wallet_data):
    # Store the wallet data in the 'wallets' dictionary using the user's ID as the key
    wallets[user_id] = wallet_data
    print(f"Wallet saved for user {user_id}")

# /set wallet button handler
@bot.message_handler(func=lambda message: message.text == "🔥 SET WALLET")
def set_wallet(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Cancel")
    bot.send_message(
        message.chat.id, "Please enter your wallet private key:", reply_markup=keyboard
    )
    bot.register_next_step_handler(message, verify_and_save_wallet)

# Verify wallet and prompt until successful
def verify_and_save_wallet(message):
    if message.text == "Cancel":
        main_menu(message.chat.id)
        return
    
    private_key = message.text.strip()
    verification_result = verify_private_key(private_key)

    if "verified" in verification_result:
        user_id = message.chat.id
        wallets[user_id] = private_key
        bot.send_message(user_id, verification_result + "\nWallet set! You can now use Auto Buy.")
        main_menu(user_id)
    else:
        bot.send_message(message.chat.id, verification_result + "\nTry again or type 'Cancel'.")

# Main menu setup
def main_menu(chat_id):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("🟢 BUY", "🔴 SELL")
    keyboard.row("🔥 SET WALLET")
    bot.send_message(chat_id, "Main Menu:", reply_markup=keyboard)

# Bot start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "Welcome to the Crypto Auto-Buyer Bot! 🚀\n\n"
        "To start, provide your wallet private key. \n\n"
        "Features: \n- Auto-buy on pump.fun and other platforms. \n\n"
        "Let's begin by setting up your wallet!"
    )
    main_menu(message.chat.id)
    bot.send_message(message.chat.id, welcome_text)

# Set webhook URL
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Ensure the webhook URL is provided
if not WEBHOOK_URL:
    raise ValueError("WEBHOOK_URL environment variable is missing.")

# Set the webhook
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)

if __name__ == '__main__':
    # Run the Flask app to handle webhook requests
    app.run(host="0.0.0.0", port=5000)
