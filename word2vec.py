# Importing necessary libraries
import pandas as pd
import numpy as np
import nltk
import csv
nltk.download('stopwords')
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import RegexpTokenizer
import re
import string
import random
from PIL import Image
import requests
from io import BytesIO
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import Word2Vec
from gensim.models.phrases import Phrases, Phraser
from matplotlib import pyplot
from gensim.models import KeyedVectors

df = pd.read_csv("F:/KGBL/BugReport/BugReport/AspectJBR/NERword2.csv")
corpus = []
for words in df['cleaned']:
    corpus.append(words.split())
# Downloading the Google pretrained Word2Vec Model

EMBEDDING_FILE = 'w2vmodel/GoogleNews-vectors-negative300.bin'
google_word2vec = KeyedVectors.load_word2vec_format(EMBEDDING_FILE, binary=True)

# Training our corpus with Google Pretrained Model

google_model = Word2Vec(size = 300, window=5, min_count = 2, workers = -1)
google_model.build_vocab(corpus)



google_model.intersect_word2vec_format(EMBEDDING_FILE, lockf=1.0, binary=True)

google_model.train(corpus, total_examples=google_model.corpus_count, epochs = 5)
#splitting the description into words


#Building TFIDF model and calculate TFIDF score

tfidf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df = 5, stop_words='english')
tfidf.fit(df['cleaned'])

# Getting the words from the TF-IDF model

tfidf_list = dict(zip(tfidf.get_feature_names(), list(tfidf.idf_)))
tfidf_feature = tfidf.get_feature_names() # tfidf words/col-names

# Building TF-IDF Word2Vec
file = "BRW2V_edit.csv"

# Storing the TFIDF Word2Vec embeddings
# tfidf_vectors = [];
sent_vectors = [];
line = 0;
# for each book description
for desc in corpus:
  # Word vectors are of zero length (Used 300 dimensions)
    sent_vec = np.zeros(300)
    print(desc)
    # num of words with a valid vector in the book description
    weight_sum =0;
    cnt_words = 0;
    for word in desc:
        if word in google_model.wv.vocab:
            vec = google_model.wv[word]
            sent_vec += vec
            cnt_words += 1
    if  cnt_words !=0 :
        sent_vec /= cnt_words
    sent_vectors.append(sent_vec)
    # for each word in the book description
    # for word in desc:
    #     if word in google_model.wv.vocab and word in tfidf_feature:
    #         vec = google_model.wv[word]
    #         tf_idf = tfidf_list[word] * (desc.count(word) / len(desc))
    #         sent_vec += (vec * tf_idf)
    #         weight_sum += tf_idf
    # if weight_sum != 0:
    #     sent_vec /= weight_sum
    # tfidf_vectors.append(sent_vec)
with open(file, 'w', encoding='utf-8', newline='') as writer1:
    writer = csv.writer(writer1)
    writer.writerow(sent_vectors)
    writer1.close()
    line += 1
    print(line)

