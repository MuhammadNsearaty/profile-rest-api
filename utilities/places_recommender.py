# -*- coding: utf-8 -*-
"""Places Recommender.ipynb

Original file is located at
    https://colab.research.google.com/drive/1XLi3rQgzKteyDKJ2GBtWA406IxT4HBxg
"""

import pickle

import pandas as pd
import numpy as np

from sklearn.neighbors import NearestNeighbors
from wikipedia2vec import Wikipedia2Vec

df = pd.read_csv('assets/Places Recommender/cleaned_wikivector_geonames.csv')

with open('assets/Places Recommender/enwiki_20180420_100d.pkl', 'rb') as f:
  wiki2vec = Wikipedia2Vec.load(f)

with open('assets/Places Recommender/geoname_wiki_vectors.npy', 'rb') as f:
    wiki_vectors = np.load(f)

with open('assets/Places Recommender/knn_model_places.pkl', 'rb') as f:
    knn = pickle.load(f)

def predict_place(wiki_title, count=10):
  _, indecies = knn.kneighbors(wiki2vec.get_entity_vector(wiki_title).reshape(1, -1), count)
  return indecies[0]

# df.iloc[predict_place('Paris')]