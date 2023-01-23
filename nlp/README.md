Python 3.10.4 | [dependencies](requirements.txt)

```shell
$ python virtualenv 3.10* defacto-nlp # create a virtual env
$ python activate defacto-nlp # activate the virtual env
$ pip install -U pip # upgrade pip in the virtual Python env
$ pip install -r requirements.txt # install the dependencies
$ python -m spacy download fr_core_news_sm # download Spacy's French-language data
```

# Word Cloud
Using the Python library [`WordCloud`](https://pypi.org/project/wordcloud/), make a word cloud from a column (`COLUMN`) in a given CSV file (`DATAFILE`).

```shell
$ python cloud.py COLUMN DATAFILE
```
![word cloud](wordcloud.png)

# LDA (pre-processing v. 1)
Using `gensim`, make an LDA model that infers a certain number of topics (`num-topics`) in the data (`DATAFILE`). The function will deliver a dynamic visualization of the topic modeling using `pyLDAvis`. The visualization should automatically open a new tab in your default web browswer. However, you can open it yourself from the absolute file path printed in the console upon the script's conclusion.
```shell
$ python simple_lda.py --num-topics 5 COLUMN DATAFILE
```
![dynamic LDA visualization in a web browswer](LDAvis_example.png)

# LDA (pre-processing v. 2)
```shell
$ python optimised_lda.py --num-topics 35 COLUMN DATAFILE
```

# TF-IDF (customized)

```shell
$ python tf_idf.py --max_df 0.2 --min_df 5 --clusters 6 --members 5 COLUMN DATAFILE
```

Customize the command with a maximum document frequency (`--max_df`, float), a minimum document frequency (`--min_df`, integer), a number of clusters (`--clusters`, integer), and the number of terms that compose a cluster (`--members`, integer).

|cluster|mem_1|mem_2|mem_3|mem_4|mem_5|
|-|-|-|-|-|-|
1|journalistes|presse|réseaux|sociaux|articles
2|information|médias information|sources|éducation|créer
3|news|fake|fake news|réseaux|réseaux sociaux
4|informations|fausses|sites|sources|sans
5|critique|esprit critique|esprit|développer|dès
6|faire|information|éducation|éducation médias|jeunes
