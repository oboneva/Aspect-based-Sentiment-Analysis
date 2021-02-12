import matplotlib.pyplot as plt
import pandas as pd


def plot(aspect_groups: list[list[str]], aspect_group_polarities):
    aspect_group_strings = [",".join(group) for group in aspect_groups]
    df = pd.DataFrame(index=aspect_group_strings)

    polarities = aspect_group_polarities.values()

    negs = [item["neg"]*100 for item in polarities]
    neus = [item["neu"]*100 for item in polarities]
    poss = [item["pos"]*100 for item in polarities]

    df["negative"] = negs
    df["neutral"] = neus
    df["positive"] = poss

    colors = ['indianred', 'gainsboro', 'seagreen']
    ax = df.plot.barh(stacked=True, figsize=(17, 7),
                      color=colors)

    for rect in ax.patches:
        height = rect.get_height()
        width = rect.get_width()
        x = rect.get_x()
        y = rect.get_y()

        label_text = f'{width:.2f}%'

        label_x = x + width / 2
        label_y = y + height / 2

        if width > 0:
            ax.text(label_x, label_y, label_text,
                    ha='center', va='center', fontsize=8)

    ax.legend(loc='upper right', borderaxespad=0.)
    ax.set_ylabel("Aspect groups", fontsize=16)
    ax.set_xlabel("Sentiments", fontsize=16)

    plt.box(False)
    plt.tight_layout(w_pad=3.5)
    plt.show()
