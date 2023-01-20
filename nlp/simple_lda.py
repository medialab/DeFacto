import os
import pickle
import click
import webbrowser

import casanova
import gensim
import gensim.corpora as corpora
import pyLDAvis
import pyLDAvis.gensim_models
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords

from prep_data import ADDITIONAL_STOPWORDS

ADDITIONAL_STOPWORDS.extend(['faut', 'information', 'informations', 'medias'])
stop_words = stopwords.words('french')
stop_words.extend(ADDITIONAL_STOPWORDS)

def sentence_to_words(sentences):
    for sentence in sentences:
        # deacc=True removes punctuations
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

    from pprint import pprint

    # number of topics
    num_topics = num_topics
    # Build LDA model
    lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                        id2word=id2word,
                                        num_topics=num_topics)
    # Print the Keyword in the 10 topics
    pprint(lda_model.print_topics())
    doc_lda = lda_model[corpus]

    # Visualize the topics
    LDAvis_data_filepath = os.path.join('ldavis_prepared_'+str(num_topics))
    # # this is a bit time consuming - make the if statement True
    # # if you want to execute visualization prep yourself
    if 1 == 1:
        LDAvis_prepared = pyLDAvis.gensim_models.prepare(lda_model, corpus, id2word)
        with open(LDAvis_data_filepath, 'wb') as f:
            pickle.dump(LDAvis_prepared, f)# load the pre-prepared pyLDAvis data from disk
    with open(LDAvis_data_filepath, 'rb') as f:
        LDAvis_prepared = pickle.load(f)
        html_path = 'ldavis_prepared_'+ str(num_topics) +'.html'
        pyLDAvis.save_html(LDAvis_prepared, html_path)

    print(f"To view the LDA visualization, open this HTML file in a web browswer: {os.path.abspath(html_path)}")
    webbrowser.open_new_tab('file:///'+os.getcwd()+'/' + html_path)







if __name__ == "__main__":
    main()