import pandas as pd

from aspect_term_extraction import aspect_term_extraction_by_pos_tagging
from sentiments_scoring import df_sentiments
from gather_info import review_aspects_polarity_mean
from aspects_filtering import filter_aspects
from aspects_to_embeddings import word2vec
from group_aspects import cluster_aspects
from data_visualisation import plot

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('words')
# nlp = spacy.load("en_core_web_sm")

REVIEW_COLUMN = "comment"

# K + O


def main():
    df = pd.read_csv("acer-reviews.csv")

    aspects = aspect_term_extraction_by_pos_tagging(df, REVIEW_COLUMN)

    aspects = filter_aspects(df, aspects, REVIEW_COLUMN, 15)

    filtered_aspects, aspects2vecs = word2vec(df, aspects, REVIEW_COLUMN)

    df_aspects = pd.DataFrame(aspects2vecs)

    aspect_groups = cluster_aspects(df_aspects, filtered_aspects, 10)

    df = df_sentiments(df, REVIEW_COLUMN, aspect_groups)

    means = review_aspects_polarity_mean(df, len(aspect_groups))

    plot(aspect_groups, means)


if __name__ == "__main__":
    main()
