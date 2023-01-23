import casanova
from nltk.corpus import stopwords
from collections import defaultdict

stoplist = stopwords.words("french")
ADDITIONAL_STOPWORDS = ["plus", "chaque", "tout", "tous", "toutes", "toute", "leur", "leurs", "comme", "afin", "pour"]
PUNCTUATION = ["»", "«", "?", "!", ".", "%", ",", ".", "(", ")", ":", "’", "&", ";" '"']


def clean_propositions(file, column)-> list[list[str]]:

    stoplist.extend(ADDITIONAL_STOPWORDS)

    frequency = defaultdict(int)

    with open(file) as f:
        reader = casanova.reader(f)

        # remove stopwords and punctuation
        texts = [
            [word for word in remove_punctuation(document).lower().split() if word not in stoplist]
            for document in reader.cells(column=column)
        ]

        # Count word frequencies
        for text in texts:
            for word in text:
                print(word)
                frequency[word] += 1

        # Only keep words that appear more than once
        processed_corpus = [[token for token in text if frequency[token] > 1] for text in texts]

        return processed_corpus


def remove_punctuation(document):
    decomposed_string = []
    for char in document:
        if char == "/" or char == "'" or char == "’": char = " "
        elif char in PUNCTUATION: char = ""
        decomposed_string.append(char)
    return "".join(decomposed_string)
