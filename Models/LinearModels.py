from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import SGDClassifier, LogisticRegressionCV
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report

PATH_TO_STOPWORDS = ""
QUANTILES_DIVIDE = 5


class LinearModels:
    def __init__(self, df, column):
        self.df = df.copy()
        self.X = self.df.article_names
        self.column = column
        self.y = self.df[column]
        self.stopwords_preparation()

    def values_transforamtion(self):
        pca = PCA(n_components=1)
        self.y = pd.DataFrame(
            pca.fit_transform(self.df[["raiting", "bookmarks", "viewers"]])
        )

    def stopwords_preparation(self):
        STOPWORDS = open(PATH_TO_STOPWORDS)
        with STOPWORDS as f:
            self.stopwords = f.read().splitlines()

    def quantile(self, y):
        for interval in self.intervals:
            if y <= interval.right:
                return interval
                break
        return interval

    def model_preparation(self):
        self.tf_vectorizer = TfidfVectorizer(
            stop_words=self.stopwords, ngram_range=(1, 2), min_df=0.001, norm="l2"
        )
        self.Xtr, self.Xval, self.ytr, self.yval = train_test_split(
            self.X, self.y, test_size=0.30, random_state=42
        )

        self.Xtr_tfidf = self.tf_vectorizer.fit_transform(self.Xtr)
        self.Xval_tfidf = self.tf_vectorizer.transform(self.Xval)

        self.ytr_quantile = pd.qcut(self.ytr, q=QUANTILES_DIVIDE)
        self.intervals = self.ytr_quantile.unique().categories.to_numpy()

        self.yval_quantile = self.yval.apply(self.quantile)

        le = LabelEncoder()
        self.ytr_quantile = le.fit_transform(self.ytr_quantile)
        self.yval_quantile = le.transform(self.yval_quantile)

    def model(self):
        self.model_preparation()
        self.logit_sgd = SGDClassifier(
            loss="log",
            shuffle=True,
            n_iter_no_change=10,
            max_iter=1000,
            penalty="l1",
            random_state=42,
        )
        self.logit_sgd.fit(self.Xtr_tfidf, self.ytr_quantile)

        print(accuracy_score(self.logit_sgd.predict(self.Xtr_tfidf), self.ytr_quantile))
        print(
            accuracy_score(self.logit_sgd.predict(self.Xval_tfidf), self.yval_quantile)
        )
        print(
            classification_report(
                self.logit_sgd.predict(self.Xval_tfidf), self.yval_quantile
            )
        )

    def visualize_coefficients(
        self, coef, feature_names, title, plot_num, n_top_features=25
    ):
        interesting_coefficients = np.argsort(coef)[-n_top_features:]

        plt.figure(figsize=(15, 15))
        plt.subplot(510 + plot_num + 1)
        colors = ["lightblue" for c in coef[interesting_coefficients]]
        plt.bar(np.arange(n_top_features), coef[interesting_coefficients], color=colors)
        feature_names = np.array(feature_names)
        plt.xticks(
            np.arange(1, 1 + n_top_features),
            feature_names[interesting_coefficients],
            rotation=60,
            ha="right",
            fontsize=14,
        )
        plt.title(title)

    def visualisation_work_model(self):
        self.model()
        titles = [
            "less interestning",
            "not interestning",
            "interestning",
            "very interestning",
            "the most interestning",
        ]
        for i in range(5):
            self.visualize_coefficients(
                self.logit_sgd.coef_[i, :],
                self.tf_vectorizer.get_feature_names(),
                title=titles[i],
                plot_num=i,
            )

    def get_predict_for_sequence(self, sequence: str):
        sequence = self.tf_vectorizer.transform([sequence])
        interval_num = list(lin.logit_sgd.predict(x))[0]
        return print(
            "Predicted count of {} between {} and {}".format(
                self.column, list(lin.intervals)[2].left, list(lin.intervals)[2].right
            )
        )
