from sentence_transformers import SentenceTransformer
import pandas as pd
import matplotlib.pyplot as plt
from prep_data import clean_propositions
from bertopic import BERTopic
import os
import gensim
import spacy

from gensim_utils import lemmatization


DATA_FILE_NAME = "../../../mieux-sinformer/mieux-sinformer.csv"
MODEL_FILE_NAME = "bertopic.model"


def pre_processing():

    # Remove stop words and punctuation
    processed_corpus = clean_propositions(DATA_FILE_NAME, column="Proposition")
        # clean_propositions() returns a nested list of tokenized, pre-processed words
        # [
        #   ['augmenter', 'publicité', 'journaux', 'papiers', 'compenser', 'hausse', 'prix', 'papier'],
        #   ['sms', 'jour', 'actualité']
        # ]

    # Create N-grams
    bigram = gensim.models.Phrases(processed_corpus, min_count=5, threshold=100)
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    data_words_bigrams = [bigram_mod[doc] for doc in processed_corpus]

    # Lemmatize N-grams
    nlp = spacy.load("fr_core_news_sm", disable=['parser', 'ner'])
    lemma_lists = lemmatization(nlp, data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

    data = [" ".join(word) for word in lemma_lists]

    return data


def main():
    data = pre_processing()

    topic_model = BERTopic(language='french', calculate_probabilities=True, verbose=True)

    topic_model.save("bertopic.model")

    # Fit model
    transformer = SentenceTransformer("dangvantuan/sentence-camembert-base")
    embeddings = transformer.encode(data)

    print(type(embeddings))
    topics, probabilities = topic_model.fit_transform(documents=data, embeddings=embeddings)

    print(topic_model.get_topic_info())

if __name__ == "__main__":
    main()