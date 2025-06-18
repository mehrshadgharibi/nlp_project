import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')


def measure_length(text):

    return len(word_tokenize(text))


def chunk_text(text, max_tokens=4000):

    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sent_tokens = word_tokenize(sentence)
        sent_length = len(sent_tokens)

        if current_length + sent_length > max_tokens and current_chunk:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_length = 0

        current_chunk.append(sentence)
        current_length += sent_length

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks