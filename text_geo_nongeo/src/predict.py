import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from datacleaning import TextPreprocessor


with open(r'C:\Users\Asus\PycharmProjects\Mehrshad\text_geo_nongeo\src\model.pkl', 'rb') as f:
    model = pickle.load(f)


vectorizer = TfidfVectorizer()
vectorizer.fit(pd.read_csv(r'C:\Users\Asus\PycharmProjects\Mehrshad\text_geo_nongeo\data\tfidf_matrix.csv').columns)


preprocessor = TextPreprocessor()


def predict(text):
    processed = preprocessor.full_preprocess(text)
    vectorized = vectorizer.transform([processed])
    prediction = model.predict(vectorized)
    return 'Geographic' if prediction[0] == 1 else 'Non-Geographic'


if __name__ == "__main__":
    sample_text = "Persian Gulf is an area in the Middle East."
    print("Prediction:", predict(sample_text))






