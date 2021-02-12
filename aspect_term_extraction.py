import nltk
import pandas as pd
import spacy

nlp = spacy.load("en_core_web_sm")


def aspect_term_extraction_by_pos_tagging(df: pd.DataFrame, text_column_name: str) -> list[str]:
    aspects = []

    df_tagged = df[text_column_name].apply(lambda review: nltk.pos_tag(
        nltk.word_tokenize(review)))

    for poss_tagged_review in df_tagged:
        for word, tag in poss_tagged_review:
            if (tag == "NN"):
                aspects.append(word)

    return aspects


def extract_opinion_modifiers(token, opinion):
    for child in token.children:
        if(child.dep_ == "advmod"):
            opinion = child.text + " " + opinion
            break

        if(child.dep_ == "det" and child.text == 'no'):
            opinion = 'not ' + opinion
            break
    return opinion


def adjective_noun_rule(review):
    doc = nlp(review)
    aspect_opinion_pairs = []

    for token in doc:
        aspect = ""
        opinion = ""

        if token.dep_ == "amod" and not token.is_stop:
            opinion = token.text
            aspect = token.head.text

        opinion = extract_opinion_modifiers(token, opinion)

        if(aspect != "" and opinion != ""):
            aspect_opinion_pairs.append((aspect, opinion))

    return aspect_opinion_pairs


def noun_adjective_rule(review):
    doc = nlp(review)
    aspect_opinion_pairs = []

    for token in doc:
        aspect = ""
        opinion = ""

        if token.dep_ == "ROOT" or token.dep_ == "ccomp" or token.dep_ == "conj":
            for child in token.children:
                if child.dep_ == "nsubj":
                    aspect = child.text

                if child.dep_ == "acomp":
                    opinion = child.text
                    opinion = extract_opinion_modifiers(child, opinion)

        if(aspect != "" and opinion != ""):
            aspect_opinion_pairs.append((aspect, opinion))

    return aspect_opinion_pairs


def aspect_term_extraction_by_rules(df: pd.DataFrame, text_column_name: str) -> list[str]:
    aspects = []

    for review in df[text_column_name]:
        aspects.append(noun_adjective_rule(review))
        aspects.append(adjective_noun_rule(review))

    flat_list = [item for sublist in aspects for item in sublist]

    return flat_list
