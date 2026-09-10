package com.example.TelegramBot;

import org.telegram.telegrambots.bots.TelegramLongPollingBot;
import org.telegram.telegrambots.meta.api.methods.send.SendDocument;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.api.methods.send.SendPhoto;
import org.telegram.telegrambots.meta.api.objects.InputFile;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.ReplyKeyboardMarkup;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.InlineKeyboardMarkup;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.buttons.KeyboardRow;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.buttons.InlineKeyboardButton;

import java.net.URL;
import java.util.ArrayList;
import java.util.List;

public class MyBot extends TelegramLongPollingBot {
    private final MyMemoryTranslator translator = new MyMemoryTranslator();
    private String currentFromLang = "en";
    private String currentToLang = "es";

    @Override
    public void onUpdateReceived(Update update) {
        if (update.hasMessage() && update.getMessage().hasText()) {
            String text = update.getMessage().getText();
            long chatId = update.getMessage().getChatId();
            String translated;
            try {
                translated = translator.translate(text, currentFromLang, currentToLang);
            } catch (Exception e) {
                throw new RuntimeException(e);
            }

            if (text.startsWith("/start")) {
                sendMainMenu(chatId);
            }
            else if (text.startsWith("/from ")) {
                currentFromLang = text.split(" ")[1];
                sendMessage(chatId, "Source language set to: " + currentFromLang);
            }
            else if (text.startsWith("/to ")) {
                currentToLang = text.split(" ")[1];
                sendMessage(chatId, "Target language set to: " + currentToLang);
            }
            else if (text.startsWith("/help")) {
                sendHelpMessage(chatId);
            }
            else if (text.startsWith("/current")) {
                String currentText = "Your current native language is set to *" + currentFromLang + "*\\.\nYour current translating language is *" + currentToLang + "*\\.\n" +
                        "To change it, write '/from en' to change 'from' language to another \\(e\\.g\\. it is en\\) and write '/to es' if you want to change 'to' lang \\(e\\.g\\. " +
                        "it is espanol\\)" +
                        "\n*In short, it is* " + currentFromLang + " \\-\\> " + currentToLang;
                sendImage(chatId, currentText);
            }
            else {
                try {

                    sendTranslatedMessageWithButtons(chatId, text, translated);
                } catch (Exception e) {
                    sendMessage(chatId, "⚠️ Error: " + e.getMessage());

                }
            }
        }
    }

    private void sendTranslatedMessageWithButtons(long chatId, String originalText, String translated) {
        InlineKeyboardMarkup navMarkup = new InlineKeyboardMarkup();
        List<List<InlineKeyboardButton>> keyboard = new ArrayList<>();

        keyboard.add(List.of(
                InlineKeyboardButton.builder().text("Original Text").callbackData(originalText).build()
        ));

        navMarkup.setKeyboard(keyboard);

        SendMessage navMessage = new SendMessage();
        navMessage.setChatId(String.valueOf(chatId));
        navMessage.setText(translated);
        navMessage.setParseMode("Markdown");
        navMessage.setReplyMarkup(navMarkup);
        try {
            execute(navMessage);
        } catch (TelegramApiException e) {
            e.printStackTrace();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }

    }
    private void sendHelpMessage(long chatId) {
        String help = "📚 Translation Bot Help:\n\n" +
                "/from [lang] - Set source language (e.g. /from en)\n" +
                "/to [lang] - Set target language (e.g. /to es)\n" +
                "Just type text to translate!\n\n" +
                "Current settings: " + currentFromLang + " → " + currentToLang;

        sendMessage(chatId, help);
    }

    private void sendMessage(long chatId, String text) {
        SendMessage message = new SendMessage();
        message.setChatId(String.valueOf(chatId));
        message.setText(text);

        try {
            execute(message);
        } catch (TelegramApiException e) {
            e.printStackTrace();
        }
    }

    @Override
    public String getBotUsername() {
        return "TranslatorByShuxrinhoBot";
    }

    @Override
    public String getBotToken() {
        return "7210184880:AAGfOyS9BGkMKP-5mrFIjLaFwEM6W56P4Go";
    }

    private void sendMainMenu(long chatId) {
        SendMessage message = new SendMessage();
        message.setChatId(chatId);
        message.setText("Welcome to my Bot! Enjoy using it. " +
                "\nContact: @Shuxrinho\n\nIf you have any problem " +
                "with language abbreviations, here is the full list " +
                "for 5 supported languages: " +
                "\nUzbek - uz \n" +
                "English - en" +
                "\nEspanol - es" +
                "\nChinese - zh" +
                "\nRussian - ru");
        ReplyKeyboardMarkup keyboardMarkup = new ReplyKeyboardMarkup();
        List<KeyboardRow> keyboard = new ArrayList<>();

        // First row
        KeyboardRow row1 = new KeyboardRow();
        row1.add("/start");
        row1.add("/help");

        // Second row
        KeyboardRow row2 = new KeyboardRow();
        row2.add("/from");
        row2.add("/to");

        KeyboardRow row3 = new KeyboardRow();
        row3.add("/current");

        // Add rows to keyboard
        keyboard.add(row1);
        keyboard.add(row2);
        keyboard.add(row3);

        // Set keyboard properties
        keyboardMarkup.setKeyboard(keyboard);
        keyboardMarkup.setResizeKeyboard(true);
        keyboardMarkup.setOneTimeKeyboard(false);
        message.setReplyMarkup(keyboardMarkup);

        try {
            execute(message);
        } catch (TelegramApiException e) {
            e.printStackTrace();
        }

    }
    private void sendImage(long chatId, String text) {
        try {
            // Step 1: Get the correct direct download URL
            String fileId = "13zDSrCP5oGMqFJ8fz0r_AtoAELjk1EJB"; // From Google Drive shareable link
            String directImageUrl = "https://drive.google.com/uc?export=view&id=" + fileId;

            SendPhoto photo = new SendPhoto();
            photo.setChatId(String.valueOf(chatId));
            photo.setPhoto(new InputFile(directImageUrl));
            photo.setCaption(text);
            photo.setParseMode("MarkdownV2");

            execute(photo);
        } catch (TelegramApiException e) {
            e.printStackTrace();
            // Fallback: Download and send as file if URL doesn't work
            try {
                sendAsDocument(chatId);
            } catch (Exception ex) {
                ex.printStackTrace();
            }
        }
    }
    private void sendAsDocument(long chatId) throws Exception {
        String fileId = "13zDSrCP5oGMqFJ8fz0r_AtoAELjk1EJB";
        URL downloadUrl = new URL("https://drive.google.com/uc?export=download&id=" + fileId);

        SendDocument document = new SendDocument();
        document.setChatId(String.valueOf(chatId));
        document.setDocument(new InputFile(downloadUrl.openStream(), "image.jpg"));
        execute(document);
    }

}