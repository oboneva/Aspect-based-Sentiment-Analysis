from statistics import mean


def review_aspects_polarity_mean(df, cluster_count: int) -> dict[str, float]:
    means = {}

    for i in range(1, cluster_count + 1):
        negs = df[f'cluster-{i}'].apply(lambda b: 0 if b is None else b["neg"])
        neus = df[f'cluster-{i}'].apply(lambda b: 0 if b is None else b["neu"])
        poss = df[f'cluster-{i}'].apply(lambda b: 0 if b is None else b["pos"])

        negs[negs != 0]
        neus[neus != 0]
        poss[poss != 0]

        means[f'cluster-{i}'] = {"neg": mean(negs),
                                 "neu": mean(neus), "pos": mean(poss)}

    return means
