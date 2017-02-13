import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download("stopwords")


class Category:
    Concert, Exhibition, Festival, Sport = range(1, 5)


regex = re.compile('[%s]' % re.escape(string.punctuation))


def cleanup(text):
    # tokenized_docs = [word.encode('utf-8') for word in text]
    tokenized_docs = [word_tokenize(doc) for doc in text]
    tokenized_docs_no_punctuation = []
    for review in tokenized_docs:
        new_review = []
        for token in review:
            new_token = regex.sub(u'', token)
            if not new_token == u'':
                new_review.append(new_token)
        tokenized_docs_no_punctuation.append(new_review)
    tokenized_docs_no_stopwords = []
    for doc in tokenized_docs_no_punctuation:
        new_term_vector = []
        for word in doc:
            if not word in stopwords.words('english'):
                new_term_vector.append(word.encode('utf-8').strip())
        tokenized_docs_no_stopwords.append(new_term_vector)
    return tokenized_docs_no_stopwords