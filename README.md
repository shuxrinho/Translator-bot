# Python Telegram Translation Bot

A Python implementation of the Telegram translation bot using **Microsoft Azure Translator API**.

## Bot Description (for Telegram - max 120 chars)

```text
🌍 Fast Translator! Send text or use /to es. Auto-detects langs, 50+ supported. Tap to copy translations! 🚀
```

---

## Project Structure

```
python_bot/
├── main.py                    # Main entry point with HTTP health check server
├── my_bot.py                  # Telegram bot implementation
├── azure_translator.py        # Microsoft Azure Translator API client
├── requirements.txt           # Python dependencies
├── .env.example              # Example environment variables file
└── README.md                  # This file
```

## Features

- **Translation**: Translates text using Microsoft Azure Translator API (2M chars/month free tier)
- **Language Selection**: Set source and target languages via commands
- **Flexible Language Input**: Accepts language codes and names (e.g., `es`, `spanish`, `espanol`)
- **Interactive Commands**: 
  - `/start` - Welcome message with keyboard
  - `/help` - Help information
  - `/from [lang]` - Set source language
  - `/to [lang]` - Set target language
  - `/current` - Show current language settings
- **Copy to Clipboard**: One-tap copy button on translated messages
- **Clear Output Format**: Shows "original → translated" format
- **Health Check Server**: HTTP endpoint for monitoring

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your credentials:
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` and add your Azure credentials:
   ```
   AZURE_TRANSLATOR_KEY=your_actual_api_key_here
   AZURE_TRANSLATOR_REGION=westus
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   ```

4. Run the bot:
   ```bash
   python main.py
   ```

## Environment Variables

- `AZURE_TRANSLATOR_KEY`: Your Microsoft Azure Translator API key (required)
- `AZURE_TRANSLATOR_REGION`: Your Azure resource region (default: `westus`)
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
- `PORT` (optional): Port for health check HTTP server (default: 8080)

## Supported Languages

Azure Translator supports 100+ languages including:
- Uzbek (uz)
- English (en)
- Spanish (es)
- Chinese (zh)
- Russian (ru)
- German (de)
- French (fr)
- Italian (it)
- Portuguese (pt)
- Japanese (ja)
- Korean (ko)
- Arabic (ar)
- Turkish (tr)

And many more! You can use language codes or names like `spanish`, `es`, `espanol`, `esp`.

## Bot Information

- **Username**: TranslatorByShuxrinhoBot
- **Contact**: @Shuxrinho

## Azure Free Tier

This bot uses Microsoft Azure Translator API which offers:
- **2 million characters per month** for free (F0 tier)
- High-quality neural machine translation
- Support for 100+ languages
- Fast response times

## Differences from Previous Version

This version has been updated to use Microsoft Azure Translator API instead of MyMemory API:
- Uses `requests` library for HTTP requests to Azure API
- Implements proper authentication with API key and region
- Higher quality translations with better context understanding
- More reliable service with better uptime
- Supports more languages with better accuracy
