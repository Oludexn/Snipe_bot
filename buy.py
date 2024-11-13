from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import logging

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace this with your bot's API token
API_TOKEN = "7937879888:AAGAFsHlKzB8Ut8vgzrEWywrGjJpi0jbX4c"

# Create an Application object using the bot token
application = Application.builder().token(API_TOKEN).build()

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

# Run the bot with an active event loop
if __name__ == '__main__':
    # Ensure that the bot's loop runs without creating a new one
    application.run_polling()
