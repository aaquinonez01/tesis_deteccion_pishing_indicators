from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, f_classif
import pandas as pd

class BodyExtractionFeature:
    def __init__(self, num_features=500):
        self.vectorizer = TfidfVectorizer()
        self.num_features = num_features
        self.selector = None

    def fit_transform(self, texts, labels):
        X = self.vectorizer.fit_transform(texts)
        self.selector = SelectKBest(f_classif, k=self.num_features)
        X_new = self.selector.fit_transform(X, labels)
        feature_names = self.vectorizer.get_feature_names_out()
        selected_feature_names = [feature_names[i] for i in self.selector.get_support(indices=True)]
        tfidf_df = pd.DataFrame(X_new.toarray(), columns=selected_feature_names)
        return tfidf_df, self.vectorizer, self.selector

    def transform(self, texts):
        X = self.vectorizer.transform(texts)
        X_new = self.selector.transform(X)
        feature_names = self.vectorizer.get_feature_names_out()
        selected_feature_names = [feature_names[i] for i in self.selector.get_support(indices=True)]
        tfidf_df = pd.DataFrame(X_new.toarray(), columns=selected_feature_names)
        return tfidf_df
