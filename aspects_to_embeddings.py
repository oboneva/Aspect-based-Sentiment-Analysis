import nltk
import gensim

WORDS = set(nltk.corpus.words.words())


def clean_review(review):
    return [w.lower() for w in nltk.wordpunct_tokenize(review) if w.lower() in WORDS]


def filter_tokens(tokens: list[str], vocabulary):
    return [token for token in tokens if token in vocabulary]


def token_to_vec(tokens: list[str], word2vec_model):
    return [word2vec_model[token] for token in tokens]


def reviews_word2vec_model(df, text_column_name: str):
    df_tokens = df[text_column_name].apply(clean_review)
    sentences = df_tokens.tolist()

    model = gensim.models.Word2Vec(sentences, min_count=1)

    return model


def word2vec(df, aspects: list[str], text_column_name: str):
    model = reviews_word2vec_model(df, text_column_name)

    filtered_tokens = filter_tokens(aspects, model.wv.vocab)

    tokens_vecs = token_to_vec(filtered_tokens, model)

    return filtered_tokens, tokens_vecs
