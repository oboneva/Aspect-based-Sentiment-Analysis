import pandas as pd
import sys

from aspect_term_extraction import aspect_term_extraction_by_pos_tagging, aspect_term_extraction_by_rules
from sentiments_scoring import df_sentiments_single_aspect_per_review, df_sentiments_by_aspect_opinion_pairs
from gather_info import review_aspects_polarity_mean
from aspects_filtering import filter_aspects
from aspects_to_embeddings import word2vec
from group_aspects import cluster_aspects
from data_visualisation import plot
from data_preprocess import clean_reviews

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('words')

REVIEW_COLUMN = "comment"
ASPECTS_COUNT = 25
ASPECT_CLUSTER_COUNT = 10

# K + O


def remove_duplicates(aspects: list[str]) -> list[str]:
    aspects = list(dict.fromkeys(aspects))

    for i in range(len(aspects)):
        for j in range(i + 1, len(aspects)):
            if aspects[i] in aspects[j]:
                aspects[i] = ""

    aspects = [aspect for aspect in aspects if aspect != ""]

    return aspects


def experiment_rules(filename: str):
    df = pd.read_csv(filename)

    aspect_opinion_pairs = aspect_term_extraction_by_rules(df, REVIEW_COLUMN)
    aspects = [aspect for aspect, _ in aspect_opinion_pairs]

    aspects = remove_duplicates(aspects)

    aspects = filter_aspects(df, aspects, REVIEW_COLUMN, ASPECTS_COUNT)

    filtered_aspects, aspects2vecs = word2vec(df, aspects, REVIEW_COLUMN)

    df_aspects = pd.DataFrame(aspects2vecs)

    aspect_groups = cluster_aspects(
        df_aspects, filtered_aspects, ASPECT_CLUSTER_COUNT)

    df = df_sentiments_by_aspect_opinion_pairs(
        df, REVIEW_COLUMN, aspect_opinion_pairs, aspect_groups)

    means = review_aspects_polarity_mean(df, len(aspect_groups))

    plot(aspect_groups, means)


def experiment_naive(filename: str):
    df = pd.read_csv(filename)

    aspects = aspect_term_extraction_by_pos_tagging(df, REVIEW_COLUMN)
    aspects = remove_duplicates(aspects)

    aspects = filter_aspects(df, aspects, REVIEW_COLUMN, ASPECTS_COUNT)

    filtered_aspects, aspects2vecs = word2vec(df, aspects, REVIEW_COLUMN)

    df_aspects = pd.DataFrame(aspects2vecs)

    aspect_groups = cluster_aspects(
        df_aspects, filtered_aspects, ASPECT_CLUSTER_COUNT)

    df = df_sentiments_single_aspect_per_review(
        df, REVIEW_COLUMN, aspect_groups)

    means = review_aspects_polarity_mean(df, len(aspect_groups))

    plot(aspect_groups, means)


def main():
    filename = sys.argv[1]

    clean_reviews(filename, REVIEW_COLUMN)
    experiment_naive(f"{filename}.csv")
    experiment_rules(f"{filename}.csv")


if __name__ == "__main__":
    main()
