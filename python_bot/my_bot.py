"""
Telegram Bot for translation using MyMemory API.
"""
import os
from telegram import Update, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram.constants import ParseMode

from my_memory_translator import MyMemoryTranslator


class MyBot:
    """A Telegram bot that translates text using MyMemory API."""
    
    BOT_TOKEN = "7210184880:AAGfOyS9BGkMKP-5mrFIjLaFwEM6W56P4Go"
    BOT_USERNAME = "TranslatorByShuxrinhoBot"
    
    def __init__(self):
        self.translator = MyMemoryTranslator()
        self.current_from_lang = "en"
        self.current_to_lang = "es"
        self.application = None
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        await self.send_main_menu(update.effective_chat.id)
        
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        chat_id = update.effective_chat.id
        help_text = (
            "📚 Translation Bot Help:\n\n"
            "/from [lang] - Set source language (e.g. /from en)\n"
            "/to [lang] - Set target language (e.g. /to es)\n"
            "Just type text to translate!\n\n"
            f"Current settings: {self.current_from_lang} → {self.current_to_lang}"
        )
        await context.bot.send_message(chat_id=chat_id, text=help_text)
        
    async def from_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /from command to set source language."""
        chat_id = update.effective_chat.id
        if context.args and len(context.args) > 0:
            self.current_from_lang = context.args[0]
            await context.bot.send_message(
                chat_id=chat_id, 
                text=f"Source language set to: {self.current_from_lang}"
            )
        else:
            await context.bot.send_message(
                chat_id=chat_id, 
                text="Please provide a language code. Example: /from en"
            )
            
    async def to_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /to command to set target language."""
        chat_id = update.effective_chat.id
        if context.args and len(context.args) > 0:
            self.current_to_lang = context.args[0]
            await context.bot.send_message(
                chat_id=chat_id, 
                text=f"Target language set to: {self.current_to_lang}"
            )
        else:
            await context.bot.send_message(
                chat_id=chat_id, 
                text="Please provide a language code. Example: /to es"
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
        await self.send_image(chat_id, current_text)
        
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming text messages."""
        if update.message and update.message.text:
            text = update.message.text
            chat_id = update.effective_chat.id
            
            # Check for commands embedded in message
            if text.startswith("/start"):
                await self.send_main_menu(chat_id)
                return
            elif text.startswith("/from "):
                parts = text.split(" ")
                if len(parts) > 1:
                    self.current_from_lang = parts[1]
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text=f"Source language set to: {self.current_from_lang}"
                    )
                return
            elif text.startswith("/to "):
                parts = text.split(" ")
                if len(parts) > 1:
                    self.current_to_lang = parts[1]
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
                await self.send_translated_message_with_buttons(
                    chat_id, 
                    text, 
                    translated
                )
            except Exception as e:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"⚠️ Error: {str(e)}"
                )
                
    async def send_translated_message_with_buttons(self, chat_id: int, original_text: str, translated: str):
        """Send translated message with inline keyboard button."""
        keyboard = [[InlineKeyboardButton("Original Text", callback_data=original_text)]]
        
        await self.application.bot.send_message(
            chat_id=chat_id,
            text=translated,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline keyboard button callbacks."""
        query = update.callback_query
        if query:
            await query.answer()
            await query.edit_message_text(text=query.data)
            
    async def send_main_menu(self, chat_id: int):
        """Send main menu with reply keyboard."""
        message_text = (
            "Welcome to my Bot! Enjoy using it. "
            "\nContact: @Shuxrinho\n\nIf you have any problem "
            "with language abbreviations, here is the full list "
            "for 5 supported languages: "
            "\nUzbek - uz \n"
            "English - en"
            "\nEspanol - es"
            "\nChinese - zh"
            "\nRussian - ru"
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
        
    async def send_image(self, chat_id: int, caption: str):
        """Send image from Google Drive with caption."""
        file_id = "13zDSrCP5oGMqFJ8fz0r_AtoAELjk1EJB"
        direct_image_url = f"https://drive.google.com/uc?export=view&id={file_id}"
        
        try:
            await self.application.bot.send_photo(
                chat_id=chat_id,
                photo=direct_image_url,
                caption=caption,
                parse_mode=ParseMode.MARKDOWN_V2
            )
        except Exception as e:
            print(f"Error sending photo: {e}")
            # Fallback: send as document
            try:
                await self.send_as_document(chat_id)
            except Exception as ex:
                print(f"Error sending document: {ex}")
                
    async def send_as_document(self, chat_id: int):
        """Send image as document (fallback method)."""
        file_id = "13zDSrCP5oGMqFJ8fz0r_AtoAELjk1EJB"
        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        
        await self.application.bot.send_document(
            chat_id=chat_id,
            document=download_url,
            filename="image.jpg"
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
