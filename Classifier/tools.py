import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import precision_score, recall_score, accuracy_score, f1_score

def load_database():
    df = pd.read_csv('./Dataframes/clf_content.csv')
    return df

def bag_of_words(content):
    model = CountVectorizer(analyzer="word", max_features=5000)
    vocabulary = model.fit_transform(content)
    return vocabulary, model

def tf_idf(content):
    model = TfidfVectorizer(analyzer="word", max_features=5000)
    vocabulary = model.fit_transform(content)
    return vocabulary, model

def evaluate(Y_true, Y_pred):
    acc_score = accuracy_score(Y_true, Y_pred)
    prec_score = precision_score(Y_true, Y_pred)
    rec_score = recall_score(Y_true, Y_pred)
    f_score = f1_score(Y_true, Y_pred)
    return [acc_score, prec_score, rec_score, f_score]