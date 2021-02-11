import nltk
import pandas as pd


def aspect_term_extraction_by_pos_tagging(df: pd.DataFrame, text_column_name: str) -> list[str]:
    aspects = []

    df_tagged = df[text_column_name].apply(lambda review: nltk.pos_tag(
        nltk.word_tokenize(review)))

    for poss_tagged_review in df_tagged:
        for word, tag in poss_tagged_review:
            if (tag == "NN"):
                aspects.append(word)

    return aspects
