package com.example.TelegramBot;

import java.net.URLEncoder;
import org.apache.http.client.methods.*;
import org.apache.http.impl.client.*;
import org.apache.http.util.EntityUtils;
import com.fasterxml.jackson.databind.ObjectMapper;

public class MyMemoryTranslator {
    private static final String API_URL = "https://api.mymemory.translated.net/get";
    private final ObjectMapper mapper = new ObjectMapper();

    public String translate(String text, String fromLang, String toLang) throws Exception {
        try {
            // Encode ALL special characters including text and language pair
            String encodedText = URLEncoder.encode(text, "UTF-8");
            String encodedLangPair = URLEncoder.encode(fromLang + "|" + toLang, "UTF-8");

            String url = String.format("%s?q=%s&langpair=%s",
                    API_URL, encodedText, encodedLangPair);

            System.out.println("Final URL: " + url); // Debug log

            try (CloseableHttpClient client = HttpClients.createDefault()) {
                HttpGet request = new HttpGet(url);

                try (CloseableHttpResponse response = client.execute(request)) {
                    String jsonResponse = EntityUtils.toString(response.getEntity());
                    return mapper.readTree(jsonResponse)
                            .path("responseData")
                            .path("translatedText")
                            .asText();
                }
            }
        } catch (Exception e) {
            System.err.println("Full error details:");
            e.printStackTrace();
            throw new Exception("Translation failed. Please try simpler text.");
        }
    }
}