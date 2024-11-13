import os
import subprocess
import git  # For cloning the repo
import shutil

# Function to check if we are in the Render environment
def is_render_environment():
    return os.path.exists("/opt/render/project/src")

# Define folder paths
if is_render_environment():
    # Render environment path
    folder_path = "/opt/render/project/src/Snipe_bot"
else:
    # Local Android path (or local testing path)
    folder_path = "/storage/emulated/0/Python/Snipe_bot"

# GitHub repository URL
repo_url = "https://github.com/Oludexn/Snipe_bot.git"
local_repo_path = "/tmp/Snipe_bot"  # Temporary directory to clone repo

# Check if the repository is already cloned
if not os.path.exists(local_repo_path):
    print("Cloning repository...")
    # Clone the repository if not already cloned
    git.Repo.clone_from(repo_url, local_repo_path)
else:
    print("Repository already cloned.")

# Set the folder_path to the cloned repository's folder
folder_path = os.path.join(local_repo_path, "Snipe_bot")

# Check if the folder_path exists
if not os.path.exists(folder_path):
    raise FileNotFoundError(f"The folder path '{folder_path}' does not exist.")

# Run each .py file in the directory (excluding masterfile.py)
for filename in os.listdir(folder_path):
    if filename.endswith(".py") and filename != "masterfile.py":  # Exclude masterfile.py itself
        file_path = os.path.join(folder_path, filename)
        print(f"Running {filename}...")
        # Run the Python file using subprocess
        result = subprocess.run(["python", file_path], capture_output=True, text=True)
        print(f"Output of {filename}:\n{result.stdout}")
        if result.stderr:
            print(f"Errors in {filename}:\n{result.stderr}")

# Start the bot after running the scripts
def start_bot():
    print("Bot is running...")
    import telebot

    # Fetch the API_KEY from the environment variable
    API_TOKEN = os.getenv("API_KEY")

    if not API_TOKEN:
        raise ValueError("API_KEY environment variable is missing.")

    # Initialize the bot with the API token
    bot = telebot.TeleBot(API_TOKEN)

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

    # Start polling (blocking)
    bot.polling(none_stop=True)

if __name__ == "__main__":
    start_bot()
