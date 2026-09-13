"""
MyMemory Translator API client for translating text.
"""
import urllib.parse
import urllib.request
import json


class MyMemoryTranslator:
    """A class to handle translation using MyMemory API."""
    
    API_URL = "https://api.mymemory.translated.net/get"
    
    def translate(self, text: str, from_lang: str, to_lang: str) -> str:
        """
        Translate text from one language to another using MyMemory API.
        
        Args:
            text: The text to translate
            from_lang: Source language code (e.g., 'en')
            to_lang: Target language code (e.g., 'es')
            
        Returns:
            The translated text
            
        Raises:
            Exception: If translation fails
        """
        try:
            # Encode ALL special characters including text and language pair
            encoded_text = urllib.parse.quote(text, safe='')
            encoded_lang_pair = urllib.parse.quote(f"{from_lang}|{to_lang}", safe='')
            
            url = f"{self.API_URL}?q={encoded_text}&langpair={encoded_lang_pair}"
            
            print(f"Final URL: {url}")  # Debug log
            
            request = urllib.request.Request(url)
            with urllib.request.urlopen(request) as response:
                json_response = response.read().decode('utf-8')
                data = json.loads(json_response)
                
                translated_text = data.get('responseData', {}).get('translatedText', '')
                return translated_text
                
        except Exception as e:
            print("Full error details:")
            print(str(e))
            raise Exception("Translation failed. Please try simpler text.")
