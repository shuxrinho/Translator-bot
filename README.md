# Python Telegram Translation Bot

A Python implementation of the Telegram translation bot originally written in Java.

## Bot Description (for Telegram - max 512 chars)

```text
🌍 Fast & Smart Translator Bot!

Instantly translate text between 50+ languages. Just send a message or use commands like /to es, /from french. Supports flexible language names (es, spanish, esp...). 

Features:
✅ Auto-detect source language
✅ Copy translation with one tap
✅ Clear "original → translated" format

Start translating now! 🚀
```

---

## Project Structure

```
python_bot/
├── main.py                    # Main entry point with HTTP health check server
├── my_bot.py                  # Telegram bot implementation
├── my_memory_translator.py    # MyMemory API translator client
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Features

- **Translation**: Translates text using MyMemory API
- **Language Selection**: Set source and target languages via commands
- **Interactive Commands**: 
  - `/start` - Welcome message with keyboard
  - `/help` - Help information
  - `/from [lang]` - Set source language
  - `/to [lang]` - Set target language
  - `/current` - Show current language settings
- **Inline Keyboard**: View original text by clicking button
- **Health Check Server**: HTTP endpoint for monitoring

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the bot:
   ```bash
   python main.py
   ```

## Environment Variables

- `PORT` (optional): Port for health check HTTP server (default: 8080)

## Supported Languages

- Uzbek (uz)
- English (en)
- Spanish (es)
- Chinese (zh)
- Russian (ru)

## Bot Information

- **Username**: TranslatorByShuxrinhoBot
- **Contact**: @Shuxrinho

## Differences from Java Version

This Python version maintains all functionality from the original Java implementation:
- Uses `python-telegram-bot` library instead of TelegramBotsApi
- Implements async/await pattern for better performance
- Uses built-in `http.server` module for health check endpoint
- Uses `urllib` for HTTP requests to MyMemory API
