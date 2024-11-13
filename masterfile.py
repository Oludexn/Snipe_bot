import os
import requests
import telebot
from flask import Flask, request

# Fetch API_KEY from environment variables
API_TOKEN = os.getenv('API_KEY')

# Initialize the bot with the API token
bot = telebot.TeleBot(API_TOKEN)

# Store auto-buy status and wallet information for each user
auto_buy_status = {}
wallets = {}

# Example save_wallet function
def save_wallet(user_id, wallet_data):
    # Store the wallet data in the 'wallets' dictionary using the user's ID as the key
    wallets[user_id] = wallet_data
    print(f"Wallet saved for user {user_id}")


# Helper function to check or set auto-buy status
def toggle_auto_buy(user_id, platform):
    if user_id not in auto_buy_status:
        auto_buy_status[user_id] = {}
    if platform not in auto_buy_status[user_id]:
        auto_buy_status[user_id][platform] = False  # default to OFF
    auto_buy_status[user_id][platform] = not auto_buy_status[user_id][platform]  # toggle the status
    return auto_buy_status[user_id][platform]

# Function to get all .py files from the GitHub repository using GitHub API
def get_python_files_from_github(repo_owner, repo_name):
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents'
    response = requests.get(url)
    if response.status_code == 200:
        files = response.json()
        py_files = [file['download_url'] for file in files if file['name'].endswith('.py')]
        return py_files
    else:
        print("Error fetching files from GitHub:", response.status_code)
        return []

# Function to download and execute a Python file dynamically
def run_python_code_from_url(file_url):
    response = requests.get(file_url)
    if response.status_code == 200:
        file_code = response.text
        exec(file_code)  # Execute the code from the downloaded file
    else:
        print(f"Failed to download {file_url}")

# Example GitHub repository details
repo_owner = 'Oludexn'  # GitHub username
repo_name = 'Snipe_bot'  # GitHub repository name

# Get all .py files from the repository
python_files = get_python_files_from_github(repo_owner, repo_name)
print("Python files in repository:", python_files)

# Run all the .py files fetched from the GitHub repository
for file_url in python_files:
    print(f"Running {file_url}")
    run_python_code_from_url(file_url)

# Flask setup for webhook handling
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

# Set webhook (Ensure the URL is correct and accessible)
bot.remove_webhook()
bot.set_webhook(url="https://snipe-bot-mq95.onrender.com/webhook")

# Start the Flask app (Make sure to use the port provided by Render)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8080)))
