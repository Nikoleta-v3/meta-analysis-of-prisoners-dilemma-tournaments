Properties of winning Iterated Prisoner's Dilemma strategies. A meta
tournament analysis.
--------------------------------------

**Authors**: [@Nikoleta-v3](https://github.com/Nikoleta-v3) [@drvinceknight](https://github.com/drvinceknight) [@marcharper](https://github.com/marcharper)

This repository contains the source code and analysis for the paper:
"Properties of winning Iterated Prisoner's Dilemma strategies" which is available at:
[arXiv:2001.05911](https://arxiv.org/abs/2001.05911).

## Software

To clone the repository locally run the following:

```
$ git clone https://github.com/Nikoleta-v3/meta-analysis-of-prisoners-dilemma-tournaments.git
```

A conda environment specifying all versions of the libraries used is given in
`environment.yml`. To create and activate the environment run:

```
$ conda env create -f environment.yml
$ source activate axlml
```

## Reproducing the results

The raw data containing the summary results of each tournament analysed in the
paper is achieved at: https://zenodo.org/record/3753498

To download and unpack the archived data run the following command whilst the
conda environment is activated:

```
$ inv data
```

To process the raw data run:

```
$ inv process
```

Note that this will take a few minutes.

The `process` task creates four data sets located in the folder `data/`:

- standard_3_processed.csv
- noise_3_processed.csv
- probend_3_processed.csv
- noise_probend_3_processed.csv

These are also available at https://zenodo.org/record/3753565.
To download the processed data sets without carrying out the `process` task run:

```
$ inv prodata
```

## Analysis

Most of the analysis presented in the paper is carried out in the Jupyter notebooks
found in the folder `nbs/`.

The analysis is also carried out the merged data set of the entire data sets
considered in the paper. To generate the merged data set run the command:

```
$ inv merge
```

To carry out the regression and correlation analysis, presented in the notebooks [3. Linear Regression](https://github.com/Nikoleta-v3/meta-analysis-of-prisoners-dilemma-tournaments/blob/master/nbs/3.%20Linear%20Regression.ipynb)
and [2. Correlation Table and Heatmaps](https://github.com/Nikoleta-v3/meta-analysis-of-prisoners-dilemma-tournaments/blob/master/nbs/2.%20Correlation%20Table%20and%20Heatmaps.ipynb), for the merged
data set run the commands:

```
$ python src/correlation.py
$ python src/regression.py
```

## Tests

Several scripts have been tested with `pytest`. To test run:

```
$ inv test
```

The software is released under an MIT license.
