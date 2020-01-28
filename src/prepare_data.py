import glob
import sys

import numpy as np
import pandas as pd

import axelrod as axl


def get_normalised_rank(row):
    return row["Rank"] / (row["size"] - 1)


def get_parameters_data_frame(directory):
    """
    A function for reading in the parameters data frame.
    """
    csv_files = glob.glob("{}parameters_*-*.csv".format(directory))
    dfs = [pd.read_csv(f) for f in csv_files]
    dfs = [
        df[["noise", "probend", "repetitions", "seed", "size", "turns"]]
        for df in dfs
    ]
    df = pd.concat(dfs, ignore_index=True)
    df = df.drop_duplicates()

    return df.sort_values(["seed"]).reset_index()


class Reader:
    """
    A class for retrieving the four data frames corresponding to each
    row of the parameters csv file.
    """

    def __init__(self, row, directory=None):
        if directory:
            self.directory = directory
        else:
            self.directory = "data/raw_data/"
        self.seed = row.seed
        self.size = row["size"]
        self.repetitions = row.repetitions
        self.noise_param = row.noise
        self.probend_param = row.probend
        self.turns_param = row.turns

    def get_noise_df(self):
        noise = pd.read_csv(
            "{}noise-data/{}.csv".format(self.directory, int(self.seed))
        )
        noise["noise"] = self.noise_param
        noise["turns"] = self.turns_param

        return noise

    def get_probend_noise_df(self):
        probend_noise = pd.read_csv(
            "{}noise-probend-data/{}.csv".format(self.directory, int(self.seed))
        )
        probend_noise["noise"] = self.noise_param
        probend_noise["probend"] = self.probend_param

        return probend_noise

    def get_standard_df(self):
        std = pd.read_csv(
            "{}std-data/{}.csv".format(self.directory, int(self.seed))
        )
        std["turns"] = self.turns_param
        return std

    def get_proend_df(self):
        probend = pd.read_csv(
            "{}probend-data/{}.csv".format(self.directory, int(self.seed))
        )
        probend["probend"] = self.probend_param

        return probend

    def common_rows(self, df):
        df["repetitions"] = self.repetitions
        df["size"] = self.size
        df["seed"] = self.seed
        df["Normalized_Rank"] = df.apply(get_normalised_rank, axis=1)

        return df


def prepare_type_dataframes(parameters_df, directory, tournament_type):
    """
    A function for reading in each of the 4 data sets for a given parameters
    row. It concats everything together and returns a pandas Data Frame.
    """
    frames = []

    if tournament_type == "standard":
        for _, row in parameters_df.iterrows():
            reader = Reader(row, directory)

            std = reader.get_standard_df()
            std = reader.common_rows(std)
            frames.append(std)

    if tournament_type == "noise":
        for _, row in parameters_df.iterrows():
            reader = Reader(row, directory)

            noise = reader.get_noise_df()
            noise = reader.common_rows(noise)
            frames.append(noise)

    if tournament_type == "probend":
        for _, row in parameters_df.iterrows():
            reader = Reader(row, directory)

            probend = reader.get_proend_df()
            probend = reader.common_rows(probend)
            frames.append(probend)

    if tournament_type == "probend_noise":
        for _, row in parameters_df.iterrows():
            reader = Reader(row, directory)

            probend_noise = reader.get_probend_noise_df()
            probend_noise = reader.common_rows(probend_noise)
            frames.append(probend_noise)

    data_frame = pd.concat(frames, ignore_index=True)

    return data_frame


if __name__ == "__main__":

    directory = sys.argv[1]
    if sys.argv[2] == "all":
        tournament_types = ["standard", "noise", "probend", "probend_noise"]
    else:
        tournament_types = sys.argv[2].split(", ")
    version = sys.argv[3]

    print("Reading parameters data frame.")
    parameters_df = get_parameters_data_frame(directory)

    for tournament_type in tournament_types:
        print("Creating & exporting %s data frame." % tournament_type)
        df = prepare_type_dataframes(parameters_df, directory, tournament_type)
        df.to_csv("data/%s_%s.csv" % (tournament_type, version))
