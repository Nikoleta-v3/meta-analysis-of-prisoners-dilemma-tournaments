"""A script for running the regression analysis on the marged data set."""
import imp

import pandas as pd
import statsmodels.api as sm

plot = imp.load_source("plot", "src/plot.py")

df =  pd.read_csv('data/merged_3_processed.csv')

features = [
    "CC_to_C_rate",
    "CD_to_C_rate",
    "DC_to_C_rate",
    "SSE",
    "Cooperation_rating_comp_to_min",
    "Cooperation_rating_comp_to_mean",
]

xs = features.copy()
X = df[xs].values
y = df['Median_score'].values

X = sm.add_constant(X)
model = sm.OLS(y, X).fit()

table = model.summary2(xname=['constant'] +xs)
rs = table.tables[0][2][0] + table.tables[0][3][0]
table = table.tables[1][['Coef.', 'P>|t|']].round(5)
table.index = ['constant'] + [plot.features_labels[index] for index in table.index[1:]]

file = open('paper/regression_merged_result_on_median_score.tex', "w")
file.write(table.round(3).to_latex().replace('\$', '$').replace('\_', ('_')))
file.close()

file = open('paper/r_square_merged_result_on_median_score.tex', "w")
file.write(rs)
file.close()
