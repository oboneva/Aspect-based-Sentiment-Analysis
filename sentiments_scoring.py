from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from statistics import mean


def score(review: str, aspects: list[str], analyzer):
    for aspect in aspects:
        if aspect in review:
            return analyzer.polarity_scores(review)
        else:
            return {'neg': 0, 'neu': 0, 'pos': 0, 'compound': 0}


def df_sentiments_single_aspect_per_review(df, text_column_name: str, aspect_clusters: list[list[str]]):
    analyzer = SentimentIntensityAnalyzer()

    for i in range(1, len(aspect_clusters) + 1):
        df[f'cluster-{i}'] = df[text_column_name].apply(
            lambda review: score(review, aspect_clusters[i - 1], analyzer))

    return df


def aspect_pairs(aspect: str, aspect_opinion_pairs: list[tuple[str, str]]):
    return [term for term, _ in aspect_opinion_pairs if term in aspect]


def score_by_pairs(review: str, aspects: list[str], aspect_opinion_pairs: list[tuple[str, str]], analyzer):
    negative_scores = []
    positive_scores = []
    neutral_scores = []
    compound_scores = []

    individual_pair_weight = 0.5
    overall_weight = 1 - individual_pair_weight

    for aspect in aspects:
        pairs_for_aspect = aspect_pairs(aspect, aspect_opinion_pairs)
        for pair in pairs_for_aspect:
            if pair[0] in review and pair[1] in review:
                score_for_pair = analyzer.polarity_scores(
                    f'{pair[0]} is {pair[1]}')
                score_for_review = analyzer.polarity_scores(review)
                negative_scores.append(
                    individual_pair_weight*score_for_pair["neg"] + overall_weight*score_for_review["neg"])
                positive_scores.append(
                    individual_pair_weight*score_for_pair["pos"] + overall_weight*score_for_review["pos"])
                neutral_scores.append(
                    individual_pair_weight*score_for_pair["neu"] + overall_weight*score_for_review["neu"])
                compound_scores.append(
                    individual_pair_weight*score_for_pair["compound"] + overall_weight*score_for_review["compound"])

    if len(negative_scores) == 0:
        return {'neg': 0, 'neu': 0, 'pos': 0, 'compound': 0}

    return {'neg': mean(negative_scores), 'neu': mean(neutral_scores),
            'pos': mean(positive_scores), 'compound': mean(compound_scores)}


def df_sentiments_by_aspect_opinion_pairs(df, text_column_name: str,
                                          aspect_opinion_pairs: list[tuple[str, str]],
                                          aspect_clusters: list[list[str]]):
    analyzer = SentimentIntensityAnalyzer()

    for i in range(1, len(aspect_clusters) + 1):
        df[f'cluster-{i}'] = df[text_column_name].apply(
            lambda review: score_by_pairs(review, aspect_clusters[i - 1],
                                          aspect_opinion_pairs, analyzer))

    return df
