import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

font = {"size": 10, "weight": "bold"}
matplotlib.rc("font", **font)

import imp

plot = imp.load_source("plot", "src/plot.py")

df = pd.read_csv("data/merged_3_processed.csv")
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
    "size",
    "turns",
    "probend",
    "noise",
    "memory_usage",
    "repetitions",
]

sort = [
    "$CC$ to $C$ rate",
    "$CD$ to $C$ rate",
    "$C_r$",
    "$C_r$ / $C_{max}$ ",
    "$C_r$ / $C_{mean}$",
    "$C_r$ / $C_{median}$",
    "$C_{max}$",
    "$C_{mean}$",
    "$C_{median}$",
    "$C_{min}$",
    "$C_{min}$ / $C_r$",
    "$DC$ to $C$ rate",
    "$DD$ to $C$ rate",
    "$N$",
    "$k$",
    "$n$",
    "$p_e$",
    "$p_n$",
    "Make use of game",
    "Make use of length",
    "SSE",
    "memory usage",
    "stochastic",
]

corr_data = df[features + clustering_on].corr()
table = corr_data[clustering_on].iloc[:-2].round(3)
table.index = [plot.features_labels[index] for index in table.index]

textfile = open("correlation_table_merged.tex", "w")
textfile.write(
    table.reindex(sort)
    .to_latex()
    .replace("\$", "$")
    .replace("\_", "_")
    .replace("\{", "{")
    .replace("\}", "}")
)
textfile.close()

corr_data = df[features + clustering_on]
corrmat = corr_data.corr()
top_corr_features = corrmat.index

data = corr_data[top_corr_features].corr().round(3)
data.columns = [plot.features_labels[feature] for feature in data.columns]
data.index = [
    plot.features_labels[feature] for feature in corr_data.corr().index
]

plt.figure(figsize=(20, 15))

sns.heatmap(data, annot=True, cmap="viridis")

plt.savefig("merged_correlation_plot.pdf", bbox_inches="tight")
