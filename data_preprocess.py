import pandas as pd
from textblob import TextBlob


def clean_reviews(filename: str, text_column_name: str):
    reviews_df = pd.read_csv(f'{filename}-raw.csv')
    reviews_df[text_column_name] = reviews_df[text_column_name].apply(
        lambda x: x.strip())

    reviews_df = reviews_df[reviews_df[text_column_name] != 'N/A']
    reviews_df = reviews_df[reviews_df[text_column_name] != 'N/a']
    reviews_df = reviews_df[reviews_df[text_column_name] != 'n/a']

    # reviews_df["filter"] = reviews_df[text_column_name].apply(
    #     lambda x: TextBlob(x).detect_language() == "en" if len(x) > 5 else False)

    # reviews_df = reviews_df.drop(
    #     reviews_df[reviews_df["filter"] == False].index)
    # reviews_df = reviews_df.drop(columns=["filter"])

    reviews_df.to_csv(f'{filename}.csv')
