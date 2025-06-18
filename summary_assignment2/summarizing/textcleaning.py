from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from utils  import measure_length, chunk_text
from collections import Counter
import nltk


def get_style_metrics(style_text):

    try:
        sentences = sent_tokenize(style_text)
        words = [word.lower() for word in word_tokenize(style_text) if word.isalnum()]

        avg_sent_len = sum(len(word_tokenize(s)) for s in sentences) / len(sentences) if sentences else 15

        stop_words = set(stopwords.words('english'))
        content_words = [word for word in words if word not in stop_words]
        word_freq = Counter(content_words)
        top_words = [word for word, _ in word_freq.most_common(50)]

        pos_tags = nltk.pos_tag(words)
        pos_dist = Counter(tag for _, tag in pos_tags)

        return {
            'avg_sentence_length': avg_sent_len,
            'frequent_words': top_words,
            'pos_distribution': pos_dist
        }
    except Exception as e:
        print(f"Error analyzing style: {e}")
        return {
            'avg_sentence_length': 15,
            'frequent_words': [],
            'pos_distribution': Counter()
        }