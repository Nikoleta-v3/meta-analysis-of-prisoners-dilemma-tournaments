import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import axelrod as axl
import dask_ml.cluster
import prepare_data


def get_strategies_properties():
    """
     A function that returns a data frame with the strategies of the Axelrod
     library and for each strategy it's property.
    """
    axl_strategies = pd.DataFrame(
        columns=[
            "Name",
            "Stochastic",
            "Memory_depth",
            "Makes_use_of_game",
            "Makes_use_of_length",
        ]
    )

    for i, strategy in enumerate(axl.strategies):
        use_of_game = 0
        use_of_length = 0

        if "game" in strategy().classifier["makes_use_of"]:
            use_of_game = 1
        if "length" in strategy().classifier["makes_use_of"]:
            use_of_length = 1
        axl_strategies.loc[i] = [
            strategy().name,
            int(strategy().classifier["stochastic"]),
            strategy().classifier["memory_depth"],
            use_of_game,
            use_of_length,
        ]
    return axl_strategies


def get_error_for_row(row):
    columns_for_sse = [
        "CC_to_C_rate",
        "CD_to_C_rate",
        "DC_to_C_rate",
        "DD_to_C_rate",
    ]
    vector = [row[column] for column in columns_for_sse]
    sse_error = prepare_data.get_least_squares(vector=vector)

    return sse_error


def get_normalised_rank(row):
    return row["Rank"] / (row["size"] - 1)


def fix_name(row):
    return row["Name"].split(":")[0]


def get_memory_percentage(row):
    if np.isinf(row["Memory_depth"]):
        return 1
    if row["Memory_depth"] == 0:
        return 0
    return row["Memory_depth"] / row["size"]


def get_cooporation_rating_compared_to_max(row):
    return row["Cooperation_rating_x"] / row["Cooperation_rating_y"]


if __name__ == "__main__":

    file = sys.argv[1]
    output = file.replace(".csv", "_processed.csv")

    replace = {"Slow Tit For Two Tats": "Tit For 2 Tats"}

    strategies_properties = get_strategies_properties()
    strategies_properties = strategies_properties.set_index("Name")

    df = pd.read_csv(file, index_col=0)

    print("Processing")
    df = df.replace(replace)
    df["SSeeror"] = df.apply(get_error_for_row, axis=1)
    df["Normalized_Rank"] = df.apply(get_normalised_rank, axis=1)
    df["Name"] = df.apply(fix_name, axis=1)
    df = pd.merge(
        df,
        strategies_properties,
        left_on="Name",
        right_index=True,
        how="left",
        sort=False,
    )
    df["Memory_usage"] = df.apply(get_memory_percentage, axis=1)

    max_coop = pd.DataFrame(df.groupby("seed")["Cooperation_rating"].max())
    df = pd.merge(
        df, max_coop, left_on="seed", right_index=True, how="left", sort=False
    )

    df["Cooperation_rating_comp_to_max"] = df.apply(
        get_cooporation_rating_compared_to_max, axis=1
    )

    to_drop = df[df["Normalized_Rank"] > 1]["seed"].unique()
    if len(to_drop) != 0:
        df = df[~(df["seed"].isin(to_drop))]

    print("Writing to file %s" % file)
    df.to_csv(output)
