import pandas as pd


def clean_reviews(filename: str, text_column_name: str):
    reviews_df = pd.read_csv(f'{filename}-raw.csv')
    reviews_df[text_column_name] = reviews_df[text_column_name].apply(
        lambda x: x.strip())
    reviews_df.to_csv(filename)
