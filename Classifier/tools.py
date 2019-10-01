import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.preprocessing import MinMaxScaler

def load_database():
    df = pd.read_csv('./Dataframes/clf_content.csv')
    return df

def bag_of_words(content):
    model = CountVectorizer(analyzer="word", max_features=5000)
    vocabulary = model.fit_transform(content)
    return vocabulary

def tf_idf(content):
    model = TfidfTransformer(analyzer="word", max_features=5000)
    vocabulary = model.fit_transform(content)
    return vocabulary