import os
import pickle
import webbrowser

import pyLDAvis
from pyLDAvis import gensim_models


def visualize_topics(num_topics, lda_model, corpus, id2word, keyword):
    if not os.path.isdir("vis"): os.mkdir("vis")

    LDAvis_data_filepath = os.path.join("vis", "ldavis_prepared_"+str(num_topics))

    if 1 == 1:
        LDAvis_prepared = gensim_models.prepare(lda_model, corpus, id2word)
        with open(LDAvis_data_filepath, "wb") as f:
            pickle.dump(LDAvis_prepared, f)
            
    # load the pre-prepared pyLDAvis data from disk
    with open(LDAvis_data_filepath, "rb") as f:
        LDAvis_prepared = pickle.load(f)
        html_path = os.path.join("vis", keyword+"_ldavis_prepared_"+ str(num_topics) +".html")
        pyLDAvis.save_html(LDAvis_prepared, html_path)

    print(f"To view the LDA visualization, open this HTML file in a web browswer: {os.path.abspath(html_path)}")
    webbrowser.open_new_tab("file:///"+os.getcwd()+"/" + html_path)


def lemmatization(nlp, texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out

