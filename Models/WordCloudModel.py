import numpy as np
from gensim import models
from gensim import corpora
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image

COUNT_OF_TOPICS = 5
PATH_TO_IMAGE = ''


class WordCloudModel:
    def __init__(self, df):
        self.df = df.copy()

    def make_bigrams(self):
        texts = self.df.article_names_lemmatize
        bigram = models.Phrases(texts, min_count=3, threshold=5)
        bigram_mod = models.phrases.Phraser(bigram)
        return [bigram_mod[doc] for doc in texts]

    def work_with_corpus(self):
        texts = self.make_bigrams()

        dictionary = corpora.Dictionary(texts)
        dictionary.filter_extremes(no_below=3, no_above=0.4)
        corpus = [dictionary.doc2bow(text) for text in texts]

        return corpus, dictionary

    def make_model(self):
        corpus, dictionary = self.work_with_corpus()
        ldamodel = models.ldamodel.LdaModel(
            corpus=corpus, id2word=dictionary, num_topics=10, passes=5
        )
        topics = ldamodel.show_topics(num_topics=10, num_words=100, formatted=False)
        return topics

    def plotwordcloud(self, topic_number):
        mask = np.array(Image.open(PATH_TO_IMAGE))
        topics = self.make_model()
        text = dict(topics[topic_number][1])
        wordcloud = WordCloud(
            background_color="white",
            max_words=100,
            width=mask.shape[1],
            height=mask.shape[0],
            collocations=False,
            mask=mask
        )
        wordcloud = wordcloud.generate_from_frequencies(text)
        plt.figure(figsize=(15, 10))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.title("Topic number {}".format(topic_number))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")

    def plot_it(self):
        for i in range(COUNT_OF_TOPICS):
            self.plotwordcloud(i)