import click
import csv
from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

from prep_data import clean_propositions

@click.command()
@click.argument("column")
@click.argument("datafile")
@click.option("--max_df", default=0.67, help="(float) threshold at which to ignore words that occur in that percentage of documents or more")
@click.option("--min_df", default=3, help="(integer) threshold at which to ignore words that occur that number of times or fewer in the corpus")
@click.option("--clusters", default=6, help="(integer) number of clusters to create")
@click.option("--members", default=8, help="(integer) number of terms to be included in one cluster")
def main(datafile, column, max_df, min_df, clusters, members):
    MAX_DF = max_df
    MIN_DF = min_df
    NO_OF_CLUSTERS = clusters
    NO_OF_MEMBERS = members
    bags_of_words = clean_propositions(datafile, column)
    data = [" ".join(bag) for bag in bags_of_words]
    result = tf_idf(data, MAX_DF, MIN_DF, NO_OF_CLUSTERS, NO_OF_MEMBERS)
    outfile_fieldnames = [f"mem_{i+1}" for i in range(int(NO_OF_MEMBERS))]
    with open("tf_idf_clusters.csv", "w") as of:
        writer = csv.writer(of)
        writer.writerow(outfile_fieldnames)
        for cluster in result:
            writer.writerow(cluster)


def tf_idf(cleaned_propositions, MAX_DF, MIN_DF, NO_OF_CLUSTERS, NO_OF_MEMBERS):

    vectorizer = TfidfVectorizer(
        lowercase=True,
        max_features=100,
        max_df=MAX_DF,
        min_df=MIN_DF,
        ngram_range=(1,3), # (tuple) include words that are either 1 token, 2 tokens (bigram) or 3 tokens (trigram)
        stop_words=stopwords.words("french")
    )

    vectors = vectorizer.fit_transform(cleaned_propositions)

    feature_names = vectorizer.get_feature_names_out()

    dense = vectors.todense()
    denselist = dense.tolist()

    all_keywords = []

    for proposition in denselist:
        x = 0
        keywords = []
        for word in proposition:
            if word > 0:
                keywords.append(feature_names[x])
            x = x+1
        all_keywords.append(keywords)
    
    true_k = NO_OF_CLUSTERS # number of clusters/topics we want

    model = KMeans(n_clusters=true_k, init="k-means++", max_iter=100, n_init=1)

    model.fit(vectors)

    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()

    clusters = []
    for i in range(true_k):
        cluster=[]
        for ind in order_centroids[i, :NO_OF_MEMBERS]:
            cluster.append(terms[ind])
        clusters.append(cluster)
    
    return clusters

if __name__ == "__main__":
    main()