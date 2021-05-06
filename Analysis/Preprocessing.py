from random import randrange
from pymystem3 import Mystem
from tqdm import tqdm
import numpy as np
import re

tqdm.pandas()

PATH_TO_RUSSIAN_STOPWORDS = ""


class ValuesPreprocessing:
    def __init__(self, df):
        self.df = df.copy()
        self.df.columns = ["article_names", "raiting", "bookmarks", "viewers"]
        self.delete_empty_values(column_name="article_names")
        self.column_values_preprocessing()
        self.apply_zero_values_changes()
        self.df.drop("index", inplace=True, axis=1)

    def delete_empty_values(self, column_name):
        self.df = self.df[self.df[column_name].notna()].copy().reset_index().copy()

    def column_values_preprocessing(self):
        self.df["viewers"] = (
            self.df["viewers"]
            .apply(lambda x: float(x[:-1].replace(" ", "").replace(",", ".")) * 1000)
            .copy()
        )
        self.df["viewers"] = self.df["viewers"].astype(int)
        self.df["raiting"] = (
            self.df["raiting"]
            .apply(lambda x: x if type(x) == float else x.replace("&plus;", ""))
            .copy()
        )
        self.df["raiting"] = self.df["raiting"].astype(float)
        self.df["bookmarks"] = self.df["bookmarks"].astype(float)

    def nan_to_zero(self, column_name):
        self.df[column_name] = np.nan_to_num(self.df[column_name], 0.0)

    def change_zero_value(self, column):
        min_ = self.df[column].iloc[self.df[column].ne(0).idxmax()]
        max_ = max(self.df[column])
        for index in range(len(self.df[column])):
            if self.df[column].iloc[index] == 0.0:
                self.df.at[index, column] = randrange(min_, max_)

    def apply_zero_values_changes(self):
        for column in ("raiting", "bookmarks"):
            self.nan_to_zero(column)
            self.change_zero_value(column)


class TextPreprocessing:
    def __init__(self, df):
        self.df = df.copy()
        self.apply_changes()
        self.lemmatization()
        self.return_columns_order()

    def strip_punctuation(self, string):
        return re.sub(r"[^\w\s]", "", str(string).lower())

    def delete_stopwords(self, text):
        stop = open(PATH_TO_RUSSIAN_STOPWORDS)
        with stop as f:
            stopwords = f.read().splitlines()
        text = text.split(" ")
        return " ".join([word for word in text if word not in stopwords])

    def apply_changes(self):
        self.df["article_names"] = self.df["article_names"].apply(
            lambda x: self.delete_stopwords(self.strip_punctuation(x))
        )

    def lemmatization(self):
        m = Mystem()
        self.df["article_names_lemmatize"] = self.df["article_names"].progress_apply(
            lambda x: m.lemmatize(x)
        )

    def return_columns_order(self):
        cols = self.df.columns.to_list()
        cols = cols[-1:] + cols[:-1]
        self.df = self.df[cols].copy()