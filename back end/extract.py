import sys,codecs
import pandas as pd
import numpy as np
import preprocessor as p
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import pickle
import re


def load_text(filename):
    with open(filename, 'rb') as filehandle:
        text = pickle.load(filehandle)
    return text

def preproccessing(text,k,query_lst=[]):
#     !pip install tweet-preprocessor    
    stop_words = list(stopwords.words('english'))
    for w in query_lst:
        stop_words.append(w)
    stop_words.append("RT")
    stop_words = set(stop_words)
    
    corpus = []
    count = 0
    doc = " "
    for t in text:
        p.set_options(p.OPT.URL, p.OPT.EMOJI,p.OPT.MENTION)
        sent = p.clean(t)
        word_tokens = word_tokenize(sent) 
        filtered_sentence = [w for w in word_tokens if not w in stop_words]
        sent = " ".join(filtered_sentence)
        
        doc+=(sent+" ")
        if (count == k):
            count = 0
            corpus.append(doc)
            doc = ""
        count += 1
    return corpus

def filter_text(text, query):
    query_nopunc = re.sub(r'[^\w\s]','', query)
    query_lst = query_nopunc.lower().split()
    query_lst += query_nopunc.split()    
    
    result = []
    for t in text:
        for q in query_lst:
            if q in t:
                result.append(t)
                break
    
    return result, query_lst

def extract_kmeans(filename,query,doc_size,true_k,n,load_model=False):
    modelfile = 'keyextraction_model.pkl'
    if (load_model):
        model = pickle.load(open(modelfile, 'rb'))
    else:
        text = load_text(filename)
        text_filtering, query_lst = filter_text(text, query)
        corpus = preproccessing(text_filtering, doc_size, query_lst)

        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(2,3))
        X = vectorizer.fit_transform(corpus)

        model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
        model.fit(X)
        
        filehandler = open(modelfile, 'wb')
        pickle.dump(model, filehandler)

    print("Top terms per cluster:")
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    result = []
    for i in range(true_k):
        print("Cluster %d:" % i),
        for ind in order_centroids[i, :n]:
            print(' %s' % terms[ind]),
            result.append(terms[ind])
        print

    print("\n")
    return list(set(result))

# if __name__ == "__main__":
#     query = "Andrew Yang"
#     print(extract_kmeans('1210election.data',query,10,3,3,True))