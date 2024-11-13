import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Fetch API Token from environment variable
API_TOKEN = os.getenv("API_KEY")

# Ensure API_TOKEN is provided
if not API_TOKEN:
    raise ValueError("API_KEY environment variable is missing.")

# Create an Application object using the bot token
application = Application.builder().token(API_TOKEN).build()

# Flask app setup for webhook
app = Flask(__name__)

# Command to start the bot and explain its functionality
async def start(update: Update, context: CallbackContext):
    message = (
        "Welcome to the Crypto Auto-Buyer Bot! 🚀\n\n"
        "This bot allows you to automatically buy newly listed coins on **pump.fun**. "
        "Once a coin is listed, the bot will place a buy order for you, ensuring you never miss a hot new coin.\n\n"
        "To get started, simply provide your wallet private key, and you'll be ready to go!\n\n"
        "Stay tuned for auto-buying and selling features coming soon! 📈"
    )
    await update.message.reply_text(message)
    
    # Print the message for the bot logs
    print("Sent /start message to user:")
    print(message)

# Set up command handlers
application.add_handler(CommandHandler('start', start))

# Webhook handler for incoming updates from Telegram
@app.route(f'/{API_TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data(as_text=True)
    update = Update.de_json(json_str, application.bot)
    application.process_update(update)
    return "OK", 200

# Set webhook URL
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Ensure the webhook URL is provided
if not WEBHOOK_URL:
    raise ValueError("WEBHOOK_URL environment variable is missing.")

# Set the webhook
application.bot.remove_webhook()
application.bot.set_webhook(url=WEBHOOK_URL)

if __name__ == '__main__':
    # Run the Flask app to handle webhook requests
    app.run(host="0.0.0.0", port=5000)
