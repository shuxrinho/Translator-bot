"""
Azure Translator API client for translating text using Microsoft Azure Cognitive Services.
"""
import requests
import uuid


class AzureTranslator:
    """A class to handle translation using Microsoft Azure Translator Text API."""
    
    API_URL = "https://api.cognitive.microsofttranslator.com/translate"
    
    def __init__(self, api_key: str, region: str):
        """
        Initialize the Azure Translator with credentials.
        
        Args:
            api_key: Your Azure Translator API key
            region: Your Azure resource region (e.g., 'westus')
        """
        self.api_key = api_key
        self.region = region
        
    def translate(self, text: str, from_lang: str, to_lang: str) -> str:
        """
        Translate text from one language to another using Azure Translator API.
        
        Args:
            text: The text to translate
            from_lang: Source language code (e.g., 'en')
            to_lang: Target language code (e.g., 'es')
            
        Returns:
            The translated text
            
        Raises:
            Exception: If translation fails
        """
        if not self.api_key:
            raise Exception("Azure Translator API key is not configured.")
        
        try:
            # Prepare the request headers
            headers = {
                'Ocp-Apim-Subscription-Key': self.api_key,
                'Ocp-Apim-Subscription-Region': self.region,
                'Content-type': 'application/json',
                'X-ClientTraceId': str(uuid.uuid4())
            }
            
            # Prepare the query parameters
            params = {
                'api-version': '3.0',
                'from': from_lang,
                'to': to_lang
            }
            
            # Prepare the request body
            body = [{'text': text}]
            
            # Make the request
            response = requests.post(
                self.API_URL,
                params=params,
                headers=headers,
                json=body
            )
            
            # Raise an error for bad status codes
            response.raise_for_status()
            
            # Parse the response
            result = response.json()
            
            # Extract the translated text
            if result and len(result) > 0:
                translations = result[0].get('translations', [])
                if translations and len(translations) > 0:
                    return translations[0]['text']
            
            raise Exception("No translation found in response.")
            
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP Error: {e.response.status_code} - {e.response.text}"
            print(f"Azure API Error: {error_msg}")
            raise Exception(f"Translation failed: {error_msg}")
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {str(e)}")
            raise Exception(f"Translation request failed: {str(e)}")
        except Exception as e:
            print(f"Unexpected Error: {str(e)}")
            raise Exception(f"Translation failed: {str(e)}")
