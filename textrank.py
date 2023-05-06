import numpy as np
import re
import networkx
import nltk


from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.tokenize import word_tokenize, sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('stopwords')
factory = StemmerFactory()
stemmer = factory.create_stemmer()
stop_words = set(stopwords.words("indonesian"))


def normalize_document(doc):
    doc = re.sub(r'[^a-zA-Z\s]', '', doc, re.I | re.A)
    doc = doc.lower()
    doc = doc.strip()
    tokens = word_tokenize(doc)
    filtered_tokens = [token for token in tokens if token not in stop_words]
    doc = ' '.join(filtered_tokens)
    return doc


normalize_corpus = np.vectorize(normalize_document)


def textRank(sentences):
    preprocessing = normalize_corpus(sentences)
    tv = TfidfVectorizer(min_df=0., max_df=1., use_idf=True)
    dt_matrix = tv.fit_transform(preprocessing)
    dt_matrix = dt_matrix.toarray()
    num_sentences = int(len(preprocessing) * 0.25)
    similarity_matrix = np.matmul(dt_matrix, dt_matrix.T)
    similarity_graph = networkx.from_numpy_array(similarity_matrix)
    scores = networkx.pagerank(similarity_graph)

    ranked_sentences = sorted(((score, index) for index, score
                               in scores.items()),
                              reverse=True)

    top_sentence_indices = [ranked_sentences[index][1]
                            for index in range(num_sentences)]
    scores = sorted(top_sentence_indices)
    summarize = [sentences[i] for i in scores[:num_sentences]]
    summarize = ' '.join(summarize)
    return summarize
