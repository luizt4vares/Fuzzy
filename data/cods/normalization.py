from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from unidecode import unidecode
import re

def remove_stop_word(text):
    stop_words = set(stopwords.words('portuguese'))
    word_tokens = word_tokenize(text)
    filtered_sentence = [w for w in word_tokens if w not in stop_words]
    text = " ".join(filtered_sentence)
    return text

def process(text:str):
    return remove_stop_word(re.sub(r'[^A-Za-z0-9\s]', '', unidecode(text.lower().strip())))