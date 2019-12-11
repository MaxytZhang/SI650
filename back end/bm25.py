import pickle
import pandas as pd
from gensim.summarization import bm25

def bm25_rank(query_str, k):
    bm = pickle.load(open("./model/bm25.pkl", 'rb'))
    average_idf = sum(map(lambda k: float(bm.idf[k]), bm.idf.keys())) / len(bm.idf.keys())
    print(average_idf)
    query = []
    for word in query_str.strip().split():
        query.append(word)
    scores = bm.get_scores(query, average_idf)

    data = pd.read_csv("./data/rank.csv")
    data["score"] = scores
    top10 = pd.unique(data.sort_values(by=['score'], ascending=False)[data['score'] != 0]["text_processed"])[:k].tolist()
    res = {
        "res": top10
    }
    return res
