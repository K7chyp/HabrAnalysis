import seaborn as sns
import warnings
import matplotlib.pyplot as plt


class Visualisation:
    def __init__(self, df):
        self.df = df.copy()

    def visualise_hist_all_columns(self):
        for column in ("raiting", "bookmarks", "viewers"):
            fig, ax = plt.subplots()
            self.df[column].hist()

    def plot_scatter(self, x_col: str, y_col: str, hue: str):
        sns.set(rc={"figure.figsize": (11.7, 8.27)})
        sns.scatterplot(data=self.df, x=x_col, y=y_col, hue=hue, palette="deep")

    def plot_boxplot(self, x_col: str, y_col: str):
        sns.boxplot(x_col, y_col, data=self.df)