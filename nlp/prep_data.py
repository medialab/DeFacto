import casanova
from nltk.corpus import stopwords

stoplist = stopwords.words("french")
ADDITIONAL_STOPWORDS = ["plus", "chaque", "tout", "tous", "toutes", "toute", "leur", "leurs", "comme", "afin", "pour"]
PUNCTUATION = ["»", "«", "?", "!", ".", "%", ",", ".", "(", ")", ":", "’", "&", ";" '"']

def clean_propositions(file, column)-> list[list[str]]:
    stoplist.extend(ADDITIONAL_STOPWORDS)
    with open(file) as f:
        reader = casanova.reader(f)
        cleaned_bags_of_words = []
        for cell in reader.cells(column):
            proposition = cell.lower()
            decomposed_proposition = []
            for char in proposition:
                if char == "/" or char == "'" or char == "’": char = " "
                elif char in PUNCTUATION: char = ""
                decomposed_proposition.append(char)
            proposition = "".join(decomposed_proposition)
            bag_of_words = [word for word in proposition.split()]
            bag_of_words = [w for w in bag_of_words if w not in stoplist]
            if bag_of_words[0] == "faut":
                bag_of_words = bag_of_words[1:]
            cleaned_bags_of_words.append(bag_of_words)
        return cleaned_bags_of_words
