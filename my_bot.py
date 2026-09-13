"""
Telegram Bot for translation using MyMemory API.
"""
import os
from telegram import Update, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, InputFile, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram.constants import ParseMode

from my_memory_translator import MyMemoryTranslator


class MyBot:
    """A Telegram bot that translates text using MyMemory API."""
    
    BOT_TOKEN = "7210184880:AAGfOyS9BGkMKP-5mrFIjLaFwEM6W56P4Go"
    BOT_USERNAME = "TranslatorByShuxrinhoBot"
    
    # Language code mappings (variations -> standard code)
    LANGUAGE_VARIATIONS = {
        'en': ['en', 'english', 'eng'],
        'es': ['es', 'spanish', 'espanol', 'esp'],
        'ru': ['ru', 'russian', 'rus'],
        'uz': ['uz', 'uzbek', 'uzb'],
        'zh': ['zh', 'chinese', 'chi', 'mandarin'],
        'de': ['de', 'german', 'ger', 'deutsch'],
        'fr': ['fr', 'french', 'fra'],
        'it': ['it', 'italian', 'ita'],
        'pt': ['pt', 'portuguese', 'por'],
        'ja': ['ja', 'japanese', 'jpn'],
        'ko': ['ko', 'korean', 'kor'],
        'ar': ['ar', 'arabic', 'ara'],
        'tr': ['tr', 'turkish', 'tur'],
    }
    
    def __init__(self):
        self.translator = MyMemoryTranslator()
        self.current_from_lang = "en"
        self.current_to_lang = "es"
        self.application = None
        self.waiting_for_from_lang = False
        self.waiting_for_to_lang = False
        
    def get_language_code(self, lang_input: str) -> str:
        """Convert language input to standard code."""
        lang_lower = lang_input.lower().strip()
        
        # Check if it's already a valid code
        for code, variations in self.LANGUAGE_VARIATIONS.items():
            if lang_lower == code or lang_lower in variations:
                return code
        
        # If no match found, return the input as-is (might be a valid code we don't have mapped)
        return lang_input
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        await self.send_main_menu(update.effective_chat.id)
        
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        chat_id = update.effective_chat.id
        help_text = (
            "📚 Translation Bot Help:\n\n"
            "/from [lang] - Set source language (e.g. /from en, /from spanish)\n"
            "/to [lang] - Set target language (e.g. /to es, /to chinese)\n"
            "Just type text to translate!\n\n"
            f"Current settings: {self.current_from_lang} → {self.current_to_lang}"
        )
        await context.bot.send_message(chat_id=chat_id, text=help_text)
        
    async def from_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /from command to set source language."""
        chat_id = update.effective_chat.id
        if context.args and len(context.args) > 0:
            lang_input = " ".join(context.args)
            self.current_from_lang = self.get_language_code(lang_input)
            await context.bot.send_message(
                chat_id=chat_id, 
                text=f"Source language set to: {self.current_from_lang}"
            )
        else:
            self.waiting_for_from_lang = True
            await context.bot.send_message(
                chat_id=chat_id, 
                text="Please send the source language name or code.\n"
                     "Examples: english, en, spanish, es, russian, ru, uzbek, uz, chinese, zh"
            )
            
    async def to_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /to command to set target language."""
        chat_id = update.effective_chat.id
        if context.args and len(context.args) > 0:
            lang_input = " ".join(context.args)
            self.current_to_lang = self.get_language_code(lang_input)
            await context.bot.send_message(
                chat_id=chat_id, 
                text=f"Target language set to: {self.current_to_lang}"
            )
        else:
            self.waiting_for_to_lang = True
            await context.bot.send_message(
                chat_id=chat_id, 
                text="Please send the target language name or code.\n"
                     "Examples: english, en, spanish, es, russian, ru, uzbek, uz, chinese, zh"
            )
            
    async def current_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /current command to show current language settings."""
        chat_id = update.effective_chat.id
        current_text = (
            f"Your current native language is set to *{self.current_from_lang}*.\n"
            f"Your current translating language is *{self.current_to_lang}*.\n"
            f"To change it, write '/from en' to change 'from' language to another (e.g. it is en) "
            f"and write '/to es' if you want to change 'to' lang (e.g. it is espanol)\n"
            f"*In short, it is* {self.current_from_lang} -> {self.current_to_lang}"
        )
        await context.bot.send_message(chat_id=chat_id, text=current_text, parse_mode=ParseMode.MARKDOWN)
        
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming text messages."""
        if update.message and update.message.text:
            text = update.message.text.strip()
            chat_id = update.effective_chat.id
            
            # Check if waiting for language input
            if self.waiting_for_from_lang:
                self.waiting_for_from_lang = False
                self.current_from_lang = self.get_language_code(text)
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"Source language set to: {self.current_from_lang}"
                )
                return
            elif self.waiting_for_to_lang:
                self.waiting_for_to_lang = False
                self.current_to_lang = self.get_language_code(text)
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"Target language set to: {self.current_to_lang}"
                )
                return
            
            # Check for commands embedded in message
            if text.startswith("/start"):
                await self.send_main_menu(chat_id)
                return
            elif text.startswith("/from "):
                parts = text.split(" ")
                if len(parts) > 1:
                    lang_input = " ".join(parts[1:])
                    self.current_from_lang = self.get_language_code(lang_input)
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text=f"Source language set to: {self.current_from_lang}"
                    )
                return
            elif text.startswith("/to "):
                parts = text.split(" ")
                if len(parts) > 1:
                    lang_input = " ".join(parts[1:])
                    self.current_to_lang = self.get_language_code(lang_input)
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text=f"Target language set to: {self.current_to_lang}"
                    )
                return
            elif text.startswith("/help"):
                await self.help_command(update, context)
                return
            elif text.startswith("/current"):
                await self.current_command(update, context)
                return
            
            # Translate the text
            try:
                translated = self.translator.translate(
                    text, 
                    self.current_from_lang, 
                    self.current_to_lang
                )
                await self.send_translated_message(
                    chat_id, 
                    text, 
                    translated
                )
            except Exception as e:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"⚠️ Error: {str(e)}"
                )
                
    async def send_translated_message(self, chat_id: int, original_text: str, translated: str):
        """Send translated message with original text and copy button."""
        result_text = f"{original_text} → {translated}"
        
        # Create inline keyboard with copy button
        keyboard = [[InlineKeyboardButton("📋 Copy Text", callback_data=f"copy:{translated}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await self.application.bot.send_message(
            chat_id=chat_id,
            text=result_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline keyboard button callbacks."""
        query = update.callback_query
        if query:
            await query.answer()
            # Handle copy button
            if query.data.startswith("copy:"):
                text_to_copy = query.data[5:]  # Remove "copy:" prefix
                await query.answer(text=text_to_copy, show_alert=False)
            
    async def send_main_menu(self, chat_id: int):
        """Send main menu with reply keyboard."""
        message_text = (
            "Welcome to the Translation Bot! 🌐\n\n"
            "I can translate text between multiple languages.\n"
            "Just type any text and I'll translate it for you!\n\n"
            "Supported languages include:\n"
            "English (en), Spanish (es), Russian (ru), Uzbek (uz), Chinese (zh)\n"
            "and many more!\n\n"
            "Contact: @Shuxrinho"
        )
        
        keyboard = [
            [KeyboardButton("/start"), KeyboardButton("/help")],
            [KeyboardButton("/from"), KeyboardButton("/to")],
            [KeyboardButton("/current")]
        ]
        
        reply_markup = ReplyKeyboardMarkup(
            keyboard, 
            resize_keyboard=True, 
            one_time_keyboard=False
        )
        
        await self.application.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=reply_markup
        )
        
    def run(self):
        """Run the bot."""
        # Create application
        self.application = Application.builder().token(self.BOT_TOKEN).build()
        
        # Add handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("from", self.from_command))
        self.application.add_handler(CommandHandler("to", self.to_command))
        self.application.add_handler(CommandHandler("current", self.current_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Start the bot
        print("Bot successfully started!")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    """Main entry point."""
    bot = MyBot()
    bot.run()


if __name__ == "__main__":
    main()
