from prep_data import clean_propositions
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import click

@click.command
@click.argument("column")
@click.argument("datafile")
def main(datafile, column):
    propositions = clean_propositions(file=datafile, column=column)

    words = [word for prop in propositions for word in prop]

    long_string = " ".join(words)

    # Create a WordCloud object
    wordcloud = WordCloud(background_color="white", max_words=1000, contour_width=3, contour_color='steelblue', width=1000, height=400)
    # Generate a word cloud
    wordcloud.generate(long_string)
    # Visualize the word cloud
    wordcloud.to_file("wordcloud.png")

    plt.figure(figsize=(20,8))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig("wordcloud.png")


if __name__ == "__main__":
    main()
