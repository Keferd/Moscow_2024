import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


def preprocess_text(text):
    text = text.lower()
    text = remove_punct(text)
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('russian'))
    tokens = [word for word in tokens if word not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    preprocessed_text = ' '.join(tokens)
    return preprocessed_text


def remove_punct(text):
    text = re.sub(r'[^\w\s-]', '', text)
    return text


def extract_number(text):
    for elem in text.split():
        if elem.isdigit():
            return elem


def clear_description(text):
    text = text.replace('• ', '', 1)
    text = text.replace('— ', '', 1)
    text = re.sub(r' •', '.', text)
    text = re.sub(r' —', '.', text)
    return text
