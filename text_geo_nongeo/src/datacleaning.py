import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from utils import load_config, batch_preprocess
import pandas as pd
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')


class TextPreprocessor:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

    def clean_text(self, text):

        text = text.lower()


        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)


        text = re.sub(r'<.*?>', '', text)


        text = text.translate(str.maketrans('', '', string.punctuation))


        text = re.sub(r'\d+', '', text)


        text = ' '.join(text.split())

        return text

    def remove_stopwords(self, text):

        words = nltk.word_tokenize(text)
        filtered_words = [word for word in words if word not in self.stop_words]
        return ' '.join(filtered_words)

    def stem_text(self, text):

        words = nltk.word_tokenize(text)
        stemmed_words = [self.stemmer.stem(word) for word in words]
        return ' '.join(stemmed_words)

    def lemmatize_text(self, text):

        words = nltk.word_tokenize(text)
        lemmatized_words = [self.lemmatizer.lemmatize(word) for word in words]
        return ' '.join(lemmatized_words)

    def full_preprocess(self, text, stem=False, lemma=True):

        text = self.clean_text(text)
        text = self.remove_stopwords(text)

        if stem:
            text = self.stem_text(text)
        elif lemma:
            text = self.lemmatize_text(text)

        return text



preprocessor = TextPreprocessor()


df = pd.read_csv(r'C:\Users\Asus\PycharmProjects\Mehrshad\text_geo_nongeo\data\wiki_dataset.csv')


df['processed_text'] = batch_preprocess(df['text'].tolist(), preprocessor)


df.to_csv(r'C:\Users\Asus\PycharmProjects\Mehrshad\text_geo_nongeo\data\processed_dataset.csv', index=False)
print(f"Processed data saved ")

