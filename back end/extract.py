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
        # p.set_options(p.OPT.URL, p.OPT.EMOJI,p.OPT.MENTION)
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
    # query_lst += query_nopunc.split()    
    
    result = []
    for t in text:
        for q in query_lst:
            if q in t.lower():
                result.append(t)
                break
    
    return result, query_lst

def extract_kmeans(filename,query,doc_size,true_k,n,load_model=False):
    modelfile = 'keyextraction_model.pkl'
    weightfile = 'word_weight.data'
    wordfile = 'term.data'
    if (load_model):
        model = pickle.load(open(modelfile, 'rb'))
        weight_dict = pickle.load(open(weightfile,'rb'))
        terms = pickle.load(open(wordfile,'rb'))
    else:
        text = load_text(filename)
        text_filtering, query_lst = filter_text(text, query)
        corpus = preproccessing(text_filtering, doc_size, query_lst)

        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(3,3))
        X = vectorizer.fit_transform(corpus)
        # save weight
        weight = vectorizer.vocabulary_.items()
        weight_dict = {}
        for w in weight:
            weight_dict[w[0]] = w[1]
        with open(weightfile, 'wb') as filehandle:
            pickle.dump(weight_dict, filehandle)
        # save terms
        terms = vectorizer.get_feature_names()
        with open(wordfile, 'wb') as filehandle:
            pickle.dump(terms, filehandle)

        model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
        model.fit(X)
        from sklearn.cluster import MeanShift
        # model = MeanShift(bandwidth=2).fit(X.toarray())
        
        
        filehandler = open(modelfile, 'wb')
        pickle.dump(model, filehandler)

    print("Top terms per cluster:")
    order_centroids = (-model.cluster_centers_).argsort()[:, ::-1]
    
    result = []
    length = true_k
    # length = len(set(model.labels_))
    term_list = []

    for i in range(length):
        print("Cluster %d:" % i),
        for ind in order_centroids[i, :n]:
            if terms[ind] not in term_list:
                print(' %s' % terms[ind])
                result.append({'word':terms[ind],'weight':str(weight_dict[terms[ind]])})
                term_list.append(terms[ind])
        print

    print("\n")
    return result

# if __name__ == "__main__":
#     query = "Andrew Yang"
#     print(extract_kmeans('1210election.data',query,10,3,10,False))