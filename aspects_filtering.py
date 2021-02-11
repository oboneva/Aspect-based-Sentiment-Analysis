from collections import Counter


def aspect_count_in_reviews(df, aspect: str, text_column_name: str):
    df_count = df[text_column_name].apply(lambda review: aspect in review)
    return df_count.value_counts()[True]

# clean: sluggish.I, '%', 't'


def is_valid(aspect: str):
    if len(aspect) < 3:
        return False
    elif "." in aspect:
        return False
    else:
        return True


def most_common_aspects(df, aspects: list[str], count: int, text_column_name: str):
    aspect_frequency_dict = {}

    for aspect in aspects:
        aspect_frequency_dict[aspect] = aspect_count_in_reviews(
            df, aspect, text_column_name)

    return Counter(aspect_frequency_dict).most_common(count)


def filter_aspects(df, aspects: list[str], text_column_name: str, count: int):
    aspects = list(dict.fromkeys(aspects))
    aspects = [aspect for aspect in aspects if is_valid(aspect)]

    aspect_count = most_common_aspects(df, aspects, count, text_column_name)

    return [aspect for aspect, _ in aspect_count]
