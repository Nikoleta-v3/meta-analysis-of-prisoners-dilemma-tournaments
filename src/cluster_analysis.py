import operator
import os
import random
import sys

import dask.array as da
import dask.dataframe as dd
import joblib
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from dask.distributed import Client
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import silhouette_score
from sklearn.model_selection import train_test_split
from sklearn.tree import export_graphviz

import dask_ml.cluster
import lime
import lime.lime_tabular
import pydot
from treeinterpreter import treeinterpreter as ti

matplotlib.use("Agg")


def cluster_analysis(data, ddf, columns, upper_n_clusters, num_of_workers):
    num_of_clusters_to_fit = range(2, upper_n_clusters)

    silhouette_avgs = {}
    for n_clusters in num_of_clusters_to_fit:
        kmeans = dask_ml.cluster.KMeans(
            n_clusters=n_clusters, random_state=0
        ).fit(data)
        ddf["Clusters: n = %s" % n_clusters] = dd.from_dask_array(
            kmeans.labels_
        )

        with joblib.parallel_backend("dask", n_jobs=num_of_workers):
            silhouette_avg = silhouette_score(
                data, kmeans.labels_, sample_size=int(len(data) * 0.001)
            )
            silhouette_avgs["Clusters: n = %s" % n_clusters] = silhouette_avg

    return ddf, silhouette_avgs, num_of_clusters_to_fit


def draw_clusters_plot(sample, upper_n_clusters, output_directory):

    fig, axes = plt.subplots(
        nrows=1, ncols=upper_n_clusters - 2, figsize=(10, 4)
    )

    x = sample["Normalized_Rank"].compute()
    y = sample["Median_score"].compute()

    for i, ax in enumerate(axes):
        ax.scatter(x, y, c=sample["Clusters: n = %s" % (i + 2)].compute())

    fig.text(0.5, 0.04, r"$r$", ha="center", weight="bold")
    fig.text(
        0.075,
        0.5,
        "median score",
        va="center",
        rotation="vertical",
        weight="bold",
    )

    plt.savefig("%sclusters_plots.pdf" % output_directory, bbox_inches="tight")
    plt.close()


def random_forest_analysis(X, y, num_of_workers, n_estimators=10):
    with joblib.parallel_backend("dask", n_jobs=num_of_workers):
        forest = RandomForestClassifier(
            n_estimators=n_estimators, random_state=0, oob_score=True
        )
        forest.fit(X, y)
        importances = forest.feature_importances_

    std = np.std(
        [tree.feature_importances_ for tree in forest.estimators_], axis=0
    )
    indices = np.argsort(importances)[::-1]

    return forest, importances, std, indices


def draw_feature_importance_bar_plot(
    X, importances, std, indices, features, output_directory
):
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
        "noise": r"$p$",
        "probend": r"$e$",
        "memory_usage": "memory usage",
        "repetitions": r"$k$",
        "size": r"$N$",

    }
    color = matplotlib.cm.viridis(0.4)
    plt.figure()
    plt.title("Feature importances")
    plt.bar(
        range(X.shape[1]),
        importances[indices],
        color=color,
        yerr=std[indices],
        align="center",
    )

    xticks = [features[f] for f in indices]
    labels = [features_labels[feature] for feature in xticks]

    plt.xticks(range(X.shape[1]), labels, rotation=90)
    plt.xlim([-1, X.shape[1]])
    plt.savefig(
        "%s_feature_importance_bar_plot.pdf" % output_directory,
        bbox_inches="tight",
    )
    plt.close()


if __name__ == "__main__":

    file = sys.argv[1]
    if len(sys.argv) > 2:
        num_of_workers = int(sys.argv[2])
    else:
        num_of_workers = 4

    input_directory = "data/%s_3_processed.csv" % file
    output_name = file.split("_3_processed")[0]

    output_directory = "output/%s/" % output_name
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    client = Client()

    df = pd.read_csv(input_directory)
    ddf = dd.from_pandas(df, npartitions=num_of_workers * 4)

    clustering_on = ["Normalized_Rank", "Median_score"]
    features = [
        "CC_to_C_rate",
        "CD_to_C_rate",
        "DC_to_C_rate",
        "DD_to_C_rate",
        "SSE",
        "Makes_use_of_game",
        "Makes_use_of_length",
        "Stochastic",
        "Cooperation_rating",
        "Cooperation_rating_max",
        "Cooperation_rating_min",
        "Cooperation_rating_median",
        "Cooperation_rating_mean",
        "Cooperation_rating_comp_to_max",
        "Cooperation_rating_comp_to_min",
        "Cooperation_rating_comp_to_median",
        "Cooperation_rating_comp_to_mean",
        "repetitions",
        "size"
    ]

    if file == "standard":
        features += ["turns", "memory_usage"]
    if file == "noise":
        features += ["noise", "turns", "memory_usage"]
    if file == "probend":
        features += ["probend"]
    if file == "probend_noise":
        features += ["probend", "noise"]

    upper_n_clusters = 5
    sample_frac = 0.05

    print("Plotting Heatmap")

    corr_data = ddf[features + clustering_on].compute(num_workers=4)
    corrmat = corr_data.corr()
    top_corr_features = corrmat.index
    plt.figure(figsize=(10, 8))

    sns.heatmap(corr_data[top_corr_features].corr(), annot=True, cmap="viridis")

    plt.savefig(
        "%s_correlation_plot.pdf" % output_directory, bbox_inches="tight"
    )
    plt.close()

    print("Clustering Analysis")
    data = ddf[clustering_on].compute(num_workers=num_of_workers)

    ddf, silhouette_avgs, num_of_clusters_to_fit = cluster_analysis(
        data, ddf, clustering_on, upper_n_clusters, num_of_workers
    )

    sample = ddf.sample(frac=sample_frac)
    draw_clusters_plot(sample, upper_n_clusters, output_directory)

    chosen_n_cluster = max(silhouette_avgs.items(), key=operator.itemgetter(1))[
        0
    ]
    output = """Analysis Output:

    number of cluster fitted: {}

    silhouette averages: {}

    chosen number of clusters: {}
    """.format(
        num_of_clusters_to_fit, silhouette_avgs, chosen_n_cluster
    )

    df = ddf[[chosen_n_cluster] + clustering_on].compute(
        num_workers=num_of_workers
    )

    medians = df.groupby(chosen_n_cluster)[clustering_on].median()
    medians.to_csv("%s_medians_table" % (output_directory))

    print("Random Forest Analysis")
    X = da.array(ddf[features].compute(num_workers=num_of_workers))
    y = da.array(ddf[chosen_n_cluster].compute(num_workers=num_of_workers))

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.33, random_state=42
    )

    random_forest, importances, std, indices = random_forest_analysis(
        X_train, y_train, num_of_workers
    )

    print("Random Forest Importance")
    output += """\nRandom Forest. Feature Importance:\n"""
    for f in range(X_train.shape[1]):
        output += "%d. feature %d: %s (%f) \n" % (
            f + 1,
            indices[f],
            features[indices[f]],
            importances[indices[f]],
        )

    draw_feature_importance_bar_plot(
        X_train, importances, std, indices, features, output_directory
    )

    with open("%sr_square_.txt" % output_directory, "w") as textfile:
        textfile.write(
            "Score on train is: %f" % random_forest.score(X_train, y_train)
            + "\n"
        )
        textfile.write(
            "Score on test is: %f" % random_forest.score(X_test, y_test) + "\n"
        )
        textfile.write("OBB score: %f" % random_forest.oob_score_ + "\n")

    textfile = open("%s_output.txt" % output_directory, "w")
    textfile.write(output)
    textfile.close()
    client.close()
