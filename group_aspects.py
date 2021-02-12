from sklearn.cluster import KMeans


def cluster_aspects(df, aspects: list[str], clusters_count: int):
    km = KMeans(n_clusters=clusters_count)
    km = km.fit(df)

    df["aspect"] = aspects
    df["cluster"] = km.labels_

    aspect_groups = df.groupby(['cluster'])['aspect'].apply(list)

    return aspect_groups
