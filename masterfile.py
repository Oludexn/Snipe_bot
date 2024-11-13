import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Initialize bot with the provided token
API_TOKEN = 'API_KEY'
bot = telebot.TeleBot(API_TOKEN)

# Store auto-buy status and wallet information for each user
auto_buy_status = {}
wallets = {}

# Helper function to check or set auto-buy status
def toggle_auto_buy(user_id, platform):
    if user_id not in auto_buy_status:
        auto_buy_status[user_id] = {}
    if platform not in auto_buy_status[user_id]:
        auto_buy_status[user_id][platform] = False  # default to OFF
    auto_buy_status[user_id][platform] = not auto_buy_status[user_id][platform]  # toggle the status
    return auto_buy_status[user_id][platform]

# Define the /start command handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "Welcome to the Crypto Auto-Buyer Bot! 🚀\n\n"
        "This bot allows you to automatically buy newly listed coins on **pump.fun**. "
        "Once a coin is listed, the bot will place a buy order for you, ensuring you never miss a hot new coin.\n\n"
        "To get started, simply provide your wallet private key, and you'll be ready to go!\n\n"
        "Stay tuned for auto-buying and selling features coming soon! 📈"
    )
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("🟢 BUY", "🔴 SELL")
    keyboard.row("🔥 SET WALLET")
    bot.send_message(message.chat.id, welcome_text, reply_markup=keyboard, parse_mode="Markdown")

# Set bot commands
bot.set_my_commands([
    telebot.types.BotCommand("start", "Initialize the Crypto Auto-Buyer Bot")
])

# /buy button handler
@bot.message_handler(func=lambda message: message.text == "🟢 BUY")
def buy(message):
    user_id = message.chat.id
    if user_id not in wallets or not wallets[user_id]:  # Check if the wallet is set
        bot.send_message(user_id, "Please set up your wallet first using the '🔥 SET WALLET' option.")
        return

    # Inline buttons for Auto Buy toggles
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(f"Raydium Auto Buy {'🟢 ON' if auto_buy_status.get(user_id, {}).get('Raydium', False) else '🔴 OFF'}", callback_data="toggle_Raydium"),
        InlineKeyboardButton(f"pump.fun Auto Buy {'🟢 ON' if auto_buy_status.get(user_id, {}).get('pump.fun', False) else '🔴 OFF'}", callback_data="toggle_pump_fun"),
        InlineKeyboardButton(f"Jupiter Auto Buy {'🟢 ON' if auto_buy_status.get(user_id, {}).get('Jupiter', False) else '🔴 OFF'}", callback_data="toggle_Jupiter")
    )
    bot.send_message(message.chat.id, "Select a platform to toggle Auto Buy:", reply_markup=markup)

# /set wallet button handler
@bot.message_handler(func=lambda message: message.text == "🔥 SET WALLET")
def set_wallet(message):
    bot.send_message(message.chat.id, "Please send your wallet private key:")
    bot.register_next_step_handler(message, save_wallet)

def save_wallet(message):
    user_id = message.chat.id
    private_key = message.text.strip()
    wallets[user_id] = private_key  # Store the private key for the user
    bot.send_message(user_id, "Wallet successfully set! You can now use the Auto Buy feature.")

# Inline button callback handler
@bot.callback_query_handler(func=lambda call: call.data.startswith("toggle_"))
def callback_toggle(call):
    user_id = call.message.chat.id
    platform = call.data.split("_")[1]  # Get platform name from callback data
    status = toggle_auto_buy(user_id, platform)  # toggle the status

    # Update inline buttons with new status
    status_text = "🟢 ON" if status else "🔴 OFF"
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(f"Raydium Auto Buy {'🟢 ON' if auto_buy_status[user_id].get('Raydium') else '🔴 OFF'}", callback_data="toggle_Raydium"),
        InlineKeyboardButton(f"pump.fun Auto Buy {'🟢 ON' if auto_buy_status[user_id].get('pump.fun') else '🔴 OFF'}", callback_data="toggle_pump_fun"),
        InlineKeyboardButton(f"Jupiter Auto Buy {'🟢 ON' if auto_buy_status[user_id].get('Jupiter') else '🔴 OFF'}", callback_data="toggle_Jupiter")
    )

    # Edit the original message to update button statuses
    bot.edit_message_text(
        "Select a platform to toggle Auto Buy:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup
    )

# Start polling
print("Bot is running...")
bot.polling(none_stop=True)