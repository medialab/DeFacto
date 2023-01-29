import os

import casanova
import click
from bertopic import BERTopic
from bertopic.vectorizers import ClassTfidfTransformer
from hdbscan import HDBSCAN
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
from umap import UMAP

TOKENIZERS_PARALLELISM=(True | False)
MODEL_FILE_NAME = "bertopic.model"
stoplist = stopwords.words("french")
ADDITIONAL_STOPWORDS = ["plus", "chaque", "tout", "tous", "toutes", "toute", "leur", "leurs", "comme", "afin", "pour"]


def special_preprocessing(string):
    string = string.lower()
    bow = string.split()
    if bow[:2] == ["il", "faut"]:
        bow = bow[2:]
    return " ".join(bow)


@click.command
@click.argument("datafile")
@click.option("-c", "--column", required=True)
def main(datafile, column):

    with open(datafile) as f:
        reader = casanova.reader(f)
        docs = [special_preprocessing(cell) for cell in reader.cells(column=column)]
        print(f"Dataset includes {len(docs)} docs.")

    if not os.path.isfile(MODEL_FILE_NAME):

        # Step 1 - Extract embeddings
        embedding_model = SentenceTransformer("dangvantuan/sentence-camembert-large")
        embeddings = embedding_model.encode(docs, show_progress_bar=True)

        # Step 2 - Reduce dimensionality
        umap_model = UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric='cosine')

        # Step 3 - Cluster reduced embeddings
        hdbscan_model = HDBSCAN(min_cluster_size=15, metric='euclidean', cluster_selection_method='eom', prediction_data=True)

        # Step 4 - Tokenize topics
        stoplist.extend(ADDITIONAL_STOPWORDS)
        vectorizer_model = CountVectorizer(stop_words=stoplist, ngram_range=(1, 2))

        # Step 5 - Create topic representation
        ctfidf_model = ClassTfidfTransformer(reduce_frequent_words=True, bm25_weighting=True)

        # Topic model
        topic_model = BERTopic(
            embedding_model=embedding_model,
            umap_model=umap_model,
            hdbscan_model=hdbscan_model,
            vectorizer_model=vectorizer_model,
            ctfidf_model=ctfidf_model,
            diversity=0.5,
            n_gram_range=(1,2),
            nr_topics='auto',
        )

        topic_model.fit_transform(documents=docs, embeddings=embeddings)

        topic_model.save(MODEL_FILE_NAME)

    # Load fitted model
    print("Opening fitted topic model.")
    topic_model = BERTopic.load(MODEL_FILE_NAME)

    topic_labels = topic_model.generate_topic_labels(nr_words=3,
                                topic_prefix=False,
                                separator=" | ")

    topic_model.set_topic_labels(topic_labels)

    topic_df = topic_model.get_topic_info()
    topic_df.to_csv('bertopic_topics.csv', index=False)

    # Generate visualizations
    vis_directory = 'bertopic_vis'
    if not os.path.isdir(vis_directory): os.mkdir(vis_directory)
    title = 'documents'
    html_path = os.path.join(vis_directory, f"{title}.html")
    png_path = os.path.join(vis_directory, f"{title}.png")
    fig = topic_model.visualize_documents(docs=docs, custom_labels=True)
    fig.write_html(html_path, auto_open=True)
    fig.write_image(png_path)

    title = 'topics'
    html_path = os.path.join(vis_directory, f"{title}.html")
    png_path = os.path.join(vis_directory, f"{title}.png")
    fig = topic_model.visualize_topics()
    fig.write_html(html_path, auto_open=True)
    fig.write_image(png_path)

    title = 'hierarchy'
    html_path = os.path.join(vis_directory, f"{title}.html")
    png_path = os.path.join(vis_directory, f"{title}.png")
    fig = topic_model.visualize_hierarchy(custom_labels=True)
    fig.write_html(html_path, auto_open=True)
    fig.write_image(png_path)

    title = 'barchart'
    html_path = os.path.join(vis_directory, f"{title}.html")
    png_path = os.path.join(vis_directory, f"{title}.png")
    fig = topic_model.visualize_barchart(custom_labels=True, n_words=10, height=600, width=600)
    fig.write_html(html_path, auto_open=True)
    fig.write_image(png_path)

    # Write document info to out-file
    results = topic_model.get_document_info(docs=docs)
    results.to_csv()
    with open(datafile) as f, open('bertopic_results.csv', 'w') as of:
        enricher = casanova.enricher(f, of, add=["document", "topic", "name", "top_n_words", "probability", "representative_document"])
        for i, row in enumerate(enricher):
            enricher.writerow(row=row, add=[results["Document"][i], results["Topic"][i], results["Name"][i], results["Top_n_words"][i], results["Probability"][i], results["Representative_document"][i]])


if __name__ == "__main__":
    main()
