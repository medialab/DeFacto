import click

import casanova
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords
from gensim_utils import visualize_topics

from prep_data import ADDITIONAL_STOPWORDS

ADDITIONAL_STOPWORDS.extend(['faut', 'information', 'informations', 'medias'])
stop_words = stopwords.words('french')
stop_words.extend(ADDITIONAL_STOPWORDS)


def sentence_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))


def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) 
             if word not in stop_words] for doc in texts]


@click.command
@click.argument("column")
@click.argument("datafile")
@click.option("--num-topics", required=True, type=int)
def main(datafile, column, num_topics):
    with open(datafile) as f:
        reader = casanova.reader(f)
        data = [cell for cell in reader.cells(column=column)]

    data_words = list(sentence_to_words(data))

    # remove stop words
    data_words = remove_stopwords(data_words)

    # Create Dictionary
    id2word = corpora.Dictionary(data_words)
    # Create Corpus
    texts = data_words
    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]

    # number of topics
    num_topics = num_topics
    # Build LDA model
    lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                        id2word=id2word,
                                        num_topics=num_topics)
    # Print the Keyword in the 10 topics
    #print(lda_model.print_topics())
    doc_lda = lda_model[corpus]

    visualize_topics(num_topics, lda_model, corpus, id2word, "simple")


if __name__ == "__main__":
    main()