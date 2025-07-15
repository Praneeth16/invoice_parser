import os
from openai import OpenAI
from dotenv import load_dotenv

class MarkdownTranslator:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(base_url=os.getenv('BASE_URL'), api_key=os.getenv("OPENAI_API_KEY"))

    def detect_language(self, text):
        """
        Detect the language of the given text using OpenAI API
        """
        try:
            response = self.client.chat.completions.create(
                model="openai/gpt-4.1",
                messages=[
                    {"role": "system", "content": "You are a language detection expert. Respond with only the ISO 639-1 language code."},
                    {"role": "user", "content": f"Detect the language of this text and respond with only the ISO 639-1 language code: {text[:1000]}"}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Error detecting language: {str(e)}")

    def translate_to_english(self, markdown_text):
        """
        Translate markdown text to English while preserving the markdown structure
        """
        try:
            # First detect the language
            source_language = self.detect_language(markdown_text)
            
            # If already English, return as is
            if source_language.lower() == 'en':
                return markdown_text

            # Prepare the translation prompt
            system_prompt = """You are a professional translator and markdown expert. 
            Your task is to translate the given markdown text to English while:
            1. Preserving all markdown syntax and formatting
            2. Maintaining the exact same structure
            3. Only translating the actual content
            4. Keeping all special characters, links, and formatting intact
            5. Preserving table structures and alignments is a must
            6. Preserving all the numbers strictly without changing the commas and decimals
            Respond with only the translated markdown text."""

            response = self.client.chat.completions.create(
                model="mistralai/mistral-medium-3",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Translate this markdown text from {source_language} to English:\n\n{markdown_text}."}
                ],
                #temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Error translating text: {str(e)}")

    def process_markdown(self, markdown_text):
        """
        Process markdown text: detect language and translate if needed
        """
        try:
            # Detect language
            source_language = self.detect_language(markdown_text)
            
            # If not English, translate
            if source_language.lower() != 'en':
                translated_text = self.translate_to_english(markdown_text)
                return {
                    'source_language': source_language,
                    'translated_text': translated_text,
                    'was_translated': True
                }
            
            return {
                'source_language': source_language,
                'translated_text': markdown_text,
                'was_translated': False
            }
            
        except Exception as e:
            raise Exception(f"Error processing markdown: {str(e)}")
