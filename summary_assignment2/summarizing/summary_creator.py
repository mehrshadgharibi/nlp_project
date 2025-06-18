from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

from utils  import measure_length, chunk_text

import nltk


def score_sentence(sentence, style_metrics):

    try:
        words = [word.lower() for word in word_tokenize(sentence) if word.isalnum()]
        if not words:
            return 0

        stop_words = set(stopwords.words('english'))
        content_words = [word for word in words if word not in stop_words]

        length_diff = abs(len(words) - style_metrics['avg_sentence_length'])
        length_score = 1 - (length_diff / style_metrics['avg_sentence_length'])

        vocab_score = sum(1 for word in content_words if word in style_metrics['frequent_words']) / len(
            content_words) if content_words else 0

        pos_tags = [tag for _, tag in nltk.pos_tag(word_tokenize(sentence))]
        pos_score = sum(style_metrics['pos_distribution'].get(tag, 0) for tag in pos_tags) / len(
            pos_tags) if pos_tags else 0

        return length_score + vocab_score + pos_score
    except Exception as e:
        print(f"Error scoring sentence: {e}")
        return 0


def summarize_with_style(content_text, style_metrics, max_sentences=10):

    try:
        sentences = sent_tokenize(content_text)
        if not sentences:
            return ""

        scored = [(sent, score_sentence(sent, style_metrics)) for sent in sentences]
        scored.sort(key=lambda x: x[1], reverse=True)
        top_sentences = [sent for sent, _ in scored[:max_sentences]]

        return ' '.join([s for s in sentences if s in top_sentences])
    except Exception as e:
        print(f"Error in summarization: {e}")
        return content_text[:1000]


def hierarchical_style_summary(text, style_metrics, target_length):

    current_text = text

    while measure_length(current_text) > target_length:
        chunks = chunk_text(current_text, target_length)
        summarized_chunks = [summarize_with_style(chunk, style_metrics) for chunk in chunks]
        current_text = ' '.join(summarized_chunks)
        if len(summarized_chunks) == 1 and measure_length(current_text) > target_length:
            break

    return current_text