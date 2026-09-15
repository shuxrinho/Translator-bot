import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv

# Import bot handlers from my_bot.py
from my_bot import TranslatorBot

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Get credentials from environment
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
azure_key = os.getenv('AZURE_TRANSLATOR_KEY')
azure_region = os.getenv('AZURE_TRANSLATOR_REGION', 'westus')

if not bot_token or not azure_key:
    logger.error("Missing TELEGRAM_BOT_TOKEN or AZURE_TRANSLATOR_KEY in environment variables.")
    raise ValueError("Missing environment variables.")

# Initialize the bot logic
translator_bot = TranslatorBot(bot_token, azure_key, azure_region)
application = translator_bot.application

@app.route(f'/bot{bot_token}/', methods=['POST'])
def telegram_webhook():
    """Handle incoming updates from Telegram."""
    try:
        update = Update.de_json(request.get_json(force=True), application.bot)
        application.update_queue.put(update)
        return 'ok'
    except Exception as e:
        logger.error(f"Error processing update: {e}")
        return 'error'

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    """Set the webhook URL. Visit this URL once to activate the bot."""
    # Use PythonAnywhere username from environment or default
    username = os.getenv('PYTHONANYWHERE_USERNAME', 'shuxratTranslatorBot')
    url = f"https://{username}.pythonanywhere.com/bot{bot_token}/"
    logger.info(f"Setting webhook to: {url}")
    
    # Remove existing webhook first to ensure clean setup
    application.bot.delete_webhook()
    
    result = application.bot.set_webhook(url=url)
    if result:
        return f"Webhook successfully set to: {url}<br><b>Note:</b> Go to PythonAnywhere Web tab and hit 'Reload' to ensure the app is running."
    else:
        return "Failed to set webhook. Check logs."

@app.route('/delete_webhook', methods=['GET'])
def delete_webhook():
    """Delete the webhook (useful for switching back to polling)."""
    result = application.bot.delete_webhook()
    if result:
        return "Webhook deleted successfully. Bot stopped."
    else:
        return "Failed to delete webhook."

@app.route('/')
def home():
    return "Translator Bot is running! Visit /set_webhook to activate."

if __name__ == '__main__':
    # For local testing only (not used on PythonAnywhere)
    app.run(port=5000, debug=True)
