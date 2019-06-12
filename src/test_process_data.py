import numpy as np
import pandas as pd

import axelrod
import process_data


def test_strategies_properties():
    df = process_data.get_strategies_properties()

    assert isinstance(df, pd.DataFrame)
    assert len(df) == len(axelrod.strategies)

    for memory_depth in df["Memory_depth"]:
        assert isinstance(memory_depth, float)

    for use_of_game in df["Makes_use_of_game"]:
        assert isinstance(use_of_game, int)

    for use_of_length in df["Makes_use_of_length"]:
        assert isinstance(use_of_length, int)


def test_get_error_for_row():
    row = {
        "CC_to_C_rate": 0,
        "CD_to_C_rate": 0,
        "DC_to_C_rate": 0,
        "DD_to_C_rate": 0,
    }
    error = process_data.get_error_for_row(row)
    assert error < 0.1


def test_get_normalised_rank():
    row = {"Rank": 1, "size": 11}
    normalised_rank = process_data.get_normalised_rank(row)

    assert normalised_rank == 0.1


def test_fix_name():
    row = {"Name": "Tit For Tat: D"}
    fixed_name = process_data.fix_name(row)

    assert fixed_name == "Tit For Tat"


def test_get_memory_percentage():
    row_example_one = {"Memory_depth": np.Infinity}
    assert process_data.get_memory_percentage(row_example_one) == 1

    row_example_one = {"Memory_depth": 0}
    assert process_data.get_memory_percentage(row_example_one) == 0

    row_example_one = {"Memory_depth": 3, "size": 10}
    assert process_data.get_memory_percentage(row_example_one) == 0.3


def get_cooporation_rating_compared_to_max(row):
    row = {"Cooperation_rating": 0.2, "Cooperation_rating_max": 0.8}

    assert process_data.get_cooporation_rating_compared_to_max(row) == 0.25
