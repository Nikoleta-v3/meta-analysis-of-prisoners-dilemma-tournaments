"""
A script to run and summarise random tournaments.

Generates:

    - <directory>/parameters.csv a csv file with parameters for each tournament
    - <directory>/data/<seed>.csv a csv file summarising a tournament for a
      given <seed>.
"""

import axelrod as axl
import pandas as pd
import random
import sys

max_size = len(axl.strategies)  # Max number of strategies
min_size = 2  # Min number of strategies

max_turns = 200
min_turns = 1

max_repetitions = 100
min_repetitions = 10

# Read the directory
try:
    directory = sys.argv[1]
except IndexError:
    directory = "../data/"

# Attempt to read directory to count number of tournaments that have been run
try:
    parameters_df = pd.read_csv("{}parameters.csv".format(directory))
    seed = int(parameters_df.seed.max() + 1)
except OSError:
    parameters_df = pd.DataFrame(columns=["seed", "turns", "repetitions"])
    seed = 0

while True:
    # Define parameter
    axl.seed(seed)
    size = random.randint(min_size, max_size)
    strategies = random.sample(axl.strategies, size)
    players = [s() for s in strategies]
    next_sample = seed + 5

    while seed < next_sample:
        # Select the strategies
        turns = random.randint(min_turns, max_turns)
        repetitions = random.randint(min_repetitions, max_repetitions)
        df = pd.DataFrame([[seed, turns, repetitions] + players],
                          columns=["seed", "turns", "repetitions"] +
                                  ["player_{}".format(i) for i in range(size)])
        parameters_df = parameters_df.append(df)

        # Run the tournament
        axl.seed(seed)
        tournament = axl.Tournament(players, turns=turns,
                                    repetitions=repetitions)
        results = tournament.play(processes=0)
        results.write_summary("{}data/{}.csv".format(directory, seed))
        parameters_df.to_csv("{}parameters.csv".format(directory))

        # Increment the seed
        seed += 1
