from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def score(review: str, aspects: list[str], analyzer):
    for aspect in aspects:
        if aspect in review:
            return analyzer.polarity_scores(review)
        else:
            return {'neg': 0, 'neu': 0, 'pos': 0, 'compound': 0}


def df_sentiments(df, text_column_name: str, aspect_clusters: list[list[str]]):
    analyzer = SentimentIntensityAnalyzer()

    for i in range(1, len(aspect_clusters) + 1):
        df[f'cluster-{i}'] = df[text_column_name].apply(
            lambda review: score(review, aspect_clusters[i - 1], analyzer))

    return df
