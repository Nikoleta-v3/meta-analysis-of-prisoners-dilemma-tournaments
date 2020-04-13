import os
import sys

import dask.array as da
import dask.dataframe as dd
import joblib
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dask.distributed import Client
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

matplotlib.use("Agg")


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
    X,
    importances,
    std,
    indices,
    features,
    output_directory,
    target_value,
    label,
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
        "noise": r"$p_n$",
        "probend": r"$p_e$",
        "repetitions": r"$k$",
        "memory_usage": "memory usage",
        "size": r"$N$",
    }
    color = matplotlib.cm.viridis(0.4)
    plt.figure()
    plt.title("Feature importances on %s" % label)
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
        "%s_feature_importance_bar_plot_%s.pdf"
        % (output_directory, target_value),
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

    output_directory = "new_output/%s/" % output_name
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    client = Client()

    df = pd.read_csv(input_directory)
    ddf = dd.from_pandas(df, npartitions=num_of_workers * 4)

    random_forest_on = ["cluster_on_0.05", "cluster_on_0.25", "cluster_on_0.5"]
    labels = ["5%", "25%", "50%"]
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

    print("Random Forest Analysis")
    for target_value, label in zip(random_forest_on, labels):
        X = da.array(ddf[features].compute(num_workers=num_of_workers))
        y = da.array(ddf[target_value].compute(num_workers=num_of_workers))

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.33, random_state=42
        )

        random_forest, importances, std, indices = random_forest_analysis(
            X_train, y_train, num_of_workers
        )

        print("Random Forest Importance")
        output = """\nRandom Forest. Feature Importance:\n"""
        for f in range(X_train.shape[1]):
            output += "%d. feature %d: %s (%f) \n" % (
                f + 1,
                indices[f],
                features[indices[f]],
                importances[indices[f]],
            )

        draw_feature_importance_bar_plot(
            X_train,
            importances,
            std,
            indices,
            features,
            output_directory,
            target_value,
            label,
        )

        with open(
            "%sr_square_%s.txt" % (output_directory, target_value), "w"
        ) as textfile:
            textfile.write(
                "Score on train is: %f" % random_forest.score(X_train, y_train)
                + "\n"
            )
            textfile.write(
                "Score on test is: %f" % random_forest.score(X_test, y_test)
                + "\n"
            )
            textfile.write("OBB score: %f" % random_forest.oob_score_ + "\n")

        textfile = open(
            "%s_output_%s.txt" % (output_directory, target_value), "w"
        )
        textfile.write(output)
        textfile.close()
    client.close()
