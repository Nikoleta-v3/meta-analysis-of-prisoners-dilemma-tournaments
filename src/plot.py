import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

c = sns.xkcd_rgb["denim blue"]


features_labels = {
    "CC_to_C_rate": "$CC$ to $C$ rate",
    "CD_to_C_rate": "$CD$ to $C$ rate",
    "DC_to_C_rate": "$DC$ to $C$ rate",
    "DD_to_C_rate": "$DD$ to $C$ rate",
    "SSE": "SSE",
    "Makes_use_of_game": "Make use of game",
    "Makes_use_of_length": "Make use of length",
    "Stochastic": "stochastic",
    "Cooperation_rating": r"$C_r$",
    "Cooperation_rating_max": r"$C_{max}$",
    "Cooperation_rating_min": r"$C_{min}$",
    "Cooperation_rating_median": r"$C_{median}$",
    "Cooperation_rating_mean": r"$C_{mean}$",
    "Cooperation_rating_comp_to_max": r"$C_r$ / $C_{max}$ ",
    "Cooperation_rating_comp_to_min": r"$C_r$ / $C_{min}$",
    "Cooperation_rating_comp_to_median": r"$C_r$ / $C_{median}$",
    "Cooperation_rating_comp_to_mean": r"$C_r$ / $C_{mean}$",
    "turns": r"$n$",
    "noise": r"$p_n$",
    "probend": r"$p_e$",
    "Normalized_Rank": r"$r$",
    "Median_score": "Median score",
    "size": r"$N$",
    "memory_usage": "memory usage",
    "repetitions": r"$k$",
}


def violin_plot(df, x, y, xlabel, ylabel, title, size=10):
    join_plot = sns.jointplot(
        x=x,
        y=y,
        data=df,
        kind="reg",
        stat_func=None,
        xlim=(0, 1),
        ylim=(0, 1),
        scatter_kws={"s": size},
    )

    plt.subplots_adjust(top=0.95)
    join_plot.fig.suptitle(title)
    join_plot.set_axis_labels(xlabel, ylabel)

    plt.show()
    return join_plot


def r_distribution(
    x,
    y1,
    y2,
    y3,
    y4,
    title,
    label1="max",
    label2="min",
    label3="mean",
    label4="median",
):
    rs = np.linspace(0, 1, 20)
    fig, axes = plt.subplots(figsize=(6, 5))
    axes.set_title(title)
    axes.set_xlabel(r"$r$")
    colormap = plt.cm.CMRmap
    plt.gca().set_color_cycle([colormap(i) for i in np.linspace(0, 0.9, 4)])
    plt.plot(rs, [sum(x >= r * y1) / len(x) for r in rs], label=label1)
    plt.plot(rs, [sum(x >= r * y2) / len(x) for r in rs], label=label2)
    plt.plot(rs, [sum(x >= r * y3) / len(x) for r in rs], label=label3)
    plt.plot(rs, [sum(x >= r * y4) / len(x) for r in rs], label=label4)
    plt.legend(loc=3)


def r_distribution_mult_types(
    x1,
    x2,
    x3,
    x4,
    y1,
    y2,
    y3,
    y4,
    title,
    label1="standard",
    label2="noisy",
    label3="probend",
    label4="noisy + probend",
    filename="fig.pdf",
):
    rs = np.linspace(0, 1, 20)
    fig, axes = plt.subplots(figsize=(6, 5))
    axes.set_title(title)
    axes.set_xlabel(r"$r$")
    colormap = plt.cm.CMRmap
    plt.gca().set_color_cycle([colormap(i) for i in np.linspace(0, 0.9, 4)])
    plt.plot(rs, [sum(x1 >= r * y1) / len(x1) for r in rs], label=label1)
    plt.plot(rs, [sum(x2 >= r * y2) / len(x2) for r in rs], label=label2)
    plt.plot(rs, [sum(x3 >= r * y3) / len(x3) for r in rs], label=label3)
    plt.plot(rs, [sum(x4 >= r * y4) / len(x4) for r in rs], label=label4)
    plt.legend(loc=3)

    plt.savefig(filename, layout="tight")
