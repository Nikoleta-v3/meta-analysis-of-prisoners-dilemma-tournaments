import prepare_data
import process_data
import axelrod
import pandas
import numpy as np


def test_specific_strategy_properties():

    df = process_data.get_strategies_properties()

    tit_for_tat = df[df["Name"] == "Tit For Tat"]
    assert tit_for_tat.Name.all() == "Tit For Tat"
    assert tit_for_tat.Memory_depth.values[0] == 1.0
    assert tit_for_tat.Stochastic.all() == 0.0
    assert tit_for_tat.Makes_use_of_game.all() == 0.0
    assert tit_for_tat.Makes_use_of_length.all() == 0.0

    adaptive = df[df["Name"] == "Adaptive"]
    assert adaptive.Name.all() == "Adaptive"
    assert adaptive.Memory_depth.values[0] == np.inf
    assert adaptive.Stochastic.all() == 0.0
    assert adaptive.Makes_use_of_game.all() == 1.0
    assert adaptive.Makes_use_of_length.all() == 0.0


parameters_df = prepare_data.get_parameters_data_frame(
    directory="data/raw_data/"
)


def test_parameters_data_frame():
    expected_columns = [
        "index",
        "noise",
        "probend",
        "repetitions",
        "seed",
        "size",
        "turns",
    ]
    assert isinstance(parameters_df, pandas.DataFrame)
    assert all(
        [
            column == expected_column
            for column, expected_column in zip(
                parameters_df.columns, expected_columns
            )
        ]
    )


def test_reader():
    row = parameters_df.sample(n=1)
    reader = prepare_data.Reader(row)

    assert reader.noise_param.values[0] == row.noise.values[0]

    assert reader.probend_param.values[0] == row.probend.values[0]
    assert reader.seed.values[0] == row.seed.values[0]
    assert reader.size.values[0] == row["size"].values[0]
    assert reader.turns_param.values[0] == row.turns.values[0]


def test_get_noise_df():
    row = parameters_df.sample(n=1)
    reader = prepare_data.Reader(row, "data/raw_data/")

    noise = reader.get_noise_df()
    assert isinstance(noise, pandas.DataFrame)
    assert all(
        [
            column in noise.columns.values
            for column in [
                "Rank",
                "Name",
                "Median_score",
                "Cooperation_rating",
                "Wins",
                "CC_rate",
                "CD_rate",
                "DC_rate",
                "DD_rate",
                "noise",
                "turns",
            ]
        ]
    )


def test_get_probend_noise_df():
    row = parameters_df.sample(n=1)
    reader = prepare_data.Reader(row, "data/raw_data/")

    probend_noise = reader.get_probend_noise_df()
    assert isinstance(probend_noise, pandas.DataFrame)
    assert all(
        [
            column in probend_noise.columns.values
            for column in [
                "Rank",
                "Name",
                "Median_score",
                "Cooperation_rating",
                "Wins",
                "CC_rate",
                "CD_rate",
                "DC_rate",
                "DD_rate",
                "noise",
                "probend",
            ]
        ]
    )


def test_get_standard_df():
    row = parameters_df.sample(n=1)
    reader = prepare_data.Reader(row, "data/raw_data/")

    std = reader.get_standard_df()
    assert isinstance(std, pandas.DataFrame)
    assert all(
        [
            column in std.columns.values
            for column in [
                "Rank",
                "Name",
                "Median_score",
                "Cooperation_rating",
                "Wins",
                "CC_rate",
                "CD_rate",
                "DC_rate",
                "DD_rate",
                "turns",
            ]
        ]
    )


def test_get_proend_df():
    row = parameters_df.sample(n=1)
    reader = prepare_data.Reader(row, "data/raw_data/")

    probend = reader.get_proend_df()
    assert isinstance(probend, pandas.DataFrame)
    assert all(
        [
            column in probend.columns.values
            for column in [
                "Rank",
                "Name",
                "Median_score",
                "Cooperation_rating",
                "Wins",
                "CC_rate",
                "CD_rate",
                "DC_rate",
                "DD_rate",
                "probend",
            ]
        ]
    )
