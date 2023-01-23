import click
import gensim
import gensim.corpora as corpora
import spacy
from casanova import namedrecord
from nltk.corpus import stopwords
import os

from prep_data import ADDITIONAL_STOPWORDS, clean_propositions
from gensim_utils import visualize_topics, lemmatization

Record = namedrecord("Record", ["document", "topics"], plural= "topics")
ADDITIONAL_STOPWORDS.extend(['faut', 'information', 'informations', 'médias', 'média', 'journaliste'])
stop_words = stopwords.words('french')
stop_words.extend(ADDITIONAL_STOPWORDS)

@click.command
@click.argument("column")
@click.argument("datafile")
@click.option("--num-topics", required=True, type=int)
def main(datafile, column, num_topics):

    # -------------------------------------------------------
    # Pre-process corpus
    with open(datafile) as f:
        processed_corpus = clean_propositions(datafile, column=column)
        # corpus is a nested list of tokenized, pre-processed words
        # corpus = [
        #   ['augmenter', 'publicité', 'journaux', 'papiers', 'compenser', 'hausse', 'prix', 'papier'],
        #   ['sms', 'jour', 'actualité']
        # ]

    # Create N-grams
    bigram = gensim.models.Phrases(processed_corpus, min_count=5, threshold=100)
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    data_words_bigrams = [bigram_mod[doc] for doc in processed_corpus]

    # Lemmatize words and N-grams
    nlp = spacy.load("fr_core_news_sm", disable=['parser', 'ner'])
    data_lemmatized = lemmatization(nlp, data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

    # -------------------------------------------------------
    # Create dictionary
    id2word = corpora.Dictionary(processed_corpus)

    # Create corpus of documents
    texts = data_lemmatized

    # Term-Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]

    # -------------------------------------------------------
    # Build or load LDA model
    if not os.path.isdir("models"): os.mkdir("models")
    model_file_name = os.path.join("models", f"lda_{num_topics}.model")

    if os.path.isfile(model_file_name):
        lda_model = gensim.models.ldamulticore.LdaMulticore.load(model_file_name)

    else:
        lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                                id2word=id2word,
                                                num_topics=num_topics, 
                                                random_state=42,
                                                chunksize=100,
                                                passes=10,
                                                per_word_topics=True,
                                                minimum_probability=0.10)
        
        lda_model.save(model_file_name)

    # -------------------------------------------------------
    # See topics the model inferred
    cluster_topics = {}
    for cluster in range(0, lda_model.num_topics-1):
        topics = lda_model.print_topic(cluster).split('"')[1::2]
        cluster_topics.update({cluster:topics})
    from pprint import pprint
    pprint(cluster_topics)

    # -------------------------------------------------------
    # Visualize the LDA model's predictions
    visualize_topics(num_topics, lda_model, corpus, id2word, "optimised")


if __name__ == "__main__":
    main()