# -*- coding: utf-8 -*-
"""Hotels Recommendation Engine.ipynb

Original file is located at
    https://colab.research.google.com/drive/1uoBBLks7nXc6hMxKLFfom-wo6S2VWk15
"""

import os
import re
import pickle

import sent2vec
import pandas as pd
import numpy as np

from nltk.tokenize.stanford import StanfordTokenizer

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder
from scipy.spatial.distance import jaccard, hamming
from sklearn.neighbors import NearestNeighbors

model = sent2vec.Sent2vecModel()
model.load_model('wiki_unigrams.bin', inference_mode=True)

allcountries_df = pd.read_csv('data_csv.csv')
cleaned_df = pd.read_csv('CleanHotelFeaturesDataset.csv')
selected_df = pd.read_csv('SelectedFeaturesHotelDataset.csv')
lower_country_name_series = allcountries_df['Name'].str.lower()

with open('countryLabelEncoder.pkl', 'rb') as f:
  le = pickle.load(f)

with open('knn_model_hotels.pkl', 'rb') as f:
  custom_knn = pickle.load(f)

tknzr = StanfordTokenizer('stanford-postagger-full-2020-11-17/stanford-postagger-4.2.0.jar', encoding='utf-8')    
  
def calc_dist(x, y):
  d1 = jaccard(x[:-1], y[:-1])
  d2 = hamming(x[-1:], y[-1:])
  return 0.8 * d1 + 0.2 * d2

def tokenize(tknzr, sentence, to_lower=True):
    """Arguments:
        - tknzr: a tokenizer implementing the NLTK tokenizer interface
        - sentence: a string to be tokenized
        - to_lower: lowercasing or not
    """
    sentence = sentence.strip()
    sentence = ' '.join([format_token(x) for x in tknzr.tokenize(sentence)])
    if to_lower:
        sentence = sentence.lower()
    sentence = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))','<url>',sentence) #replace urls by <url>
    sentence = re.sub('(\@[^\s]+)','<user>',sentence) #replace @user268 by <user>
    filter(lambda word: ' ' not in word, sentence)
    return sentence

def format_token(token):
    """"""
    if token == '-LRB-':
        token = '('
    elif token == '-RRB-':
        token = ')'
    elif token == '-RSB-':
        token = ']'
    elif token == '-LSB-':
        token = '['
    elif token == '-LCB-':
        token = '{'
    elif token == '-RCB-':
        token = '}'
    return token

def tokenize_sentences(tknzr, sentences, to_lower=True):
    """Arguments:
        - tknzr: a tokenizer implementing the NLTK tokenizer interface
        - sentences: a list of sentences
        - to_lower: lowercasing or not
    """
    return [tokenize(tknzr, s, to_lower) for s in sentences]

def get_sentence_embeddings(sentences):
    """ Returns a numpy matrix of embeddings for one of the published models. It
    handles tokenization and can be given raw sentences.
    Arguments:
        - sentences: a list of raw sentences ['Once upon a time', 'This is another sentence.', ...]
    """
    
    s = ' <delimiter> '.join(sentences) #just a trick to make things faster

    tokenized_sentences_SNLP = tokenize_sentences(tknzr, [s])
    tokenized_sentences_SNLP = tokenized_sentences_SNLP[0].split(' <delimiter> ')

    assert(len(tokenized_sentences_SNLP) == len(sentences))
    
    return model.embed_sentences(tokenized_sentences_SNLP)

selected_features_embeddings = get_sentence_embeddings(selected_df.columns.drop('country'))

def vectorize(features, country):
  similarity = cosine_similarity(selected_features_embeddings, get_sentence_embeddings(features))
  where = np.where(similarity + 1e-4 > 0.6)

  v = np.zeros((selected_df.shape[1], ), dtype=np.int16)

  v[where[0]] = 1
  
  res = allcountries_df[(lower_country_name_series.str.find(country.lower()) != -1)]

  if not res.empty:
    v[-1] = le.transform(res['Name'])[0]
  else:
    v[-1] = -1
  
  return v.reshape(1, -1)

def predict_api(features, country, count = 10):
  v = vectorize(features, country)
  _ ,indecies = custom_knn.kneighbors(v, count)
  return indecies[0]

def predict_local(hotel_index, count = 10):
  _,indecies = custom_knn.kneighbors(selected_df.iloc[hotel_index].to_numpy().reshape(1, -1), count + 1)
  return indecies[0][1:]