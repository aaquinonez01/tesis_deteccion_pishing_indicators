import re
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

# Descargar recursos necesarios para NLTK
nltk.download("punkt")
nltk.download("stopwords")


class TextProcessor:
    def __init__(self):
        self.stop_words = set(stopwords.words("english"))

    def preprocess_text(self, text):
        text = self.remove_html(text)
        text = self.remove_punctuation_and_special_chars(text)
        text = self.convert_to_lowercase(text)
        tokens = self.tokenize(text)
        tokens = self.remove_stop_words(tokens)
        return tokens

    def remove_html(self, text):
        soup = BeautifulSoup(text, "html.parser")
        return soup.get_text()

    def remove_punctuation_and_special_chars(self, text):
        return re.sub(r"\W", " ", text)

    def convert_to_lowercase(self, text):
        return text.lower()

    def tokenize(self, text):
        return word_tokenize(text)

    def remove_stop_words(self, tokens):
        return [word for word in tokens if word not in self.stop_words]
