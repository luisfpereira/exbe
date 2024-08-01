import numpy as np
from matplotlib import pyplot as plt


def bar_plot(x, y, ax=None, width=0.35, multiple=False):
    if ax is None:
        _, ax = plt.subplots()

    ind = np.arange(len(x))

    if multiple:
        val = ind - width * ((len(y) / 2) + 1 / 2)
        for index, y_ in enumerate(y):
            ax.bar(
                val + width * (index + 1),
                np.mean(y_, axis=-1),
                width,
                yerr=np.std(y_, axis=-1),
            )

    else:
        ax.bar(
            ind,
            np.mean(y, axis=-1),
            yerr=np.std(y, axis=-1),
        )

    ax.set_xticks(ind)
    ax.set_xticklabels(x)

    return ax
