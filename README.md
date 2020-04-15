Properties of winning Iterated Prisoner's Dilemma strategies. A meta
tournament analysis.
--------------------------------------

**Authors**: [@Nikoleta-v3](https://github.com/Nikoleta-v3) [@drvinceknight](https://github.com/drvinceknight) [@marcharper](https://github.com/marcharper)

This repository contains the source code and analysis for a paper titled:
"Properties of winning Iterated Prisoner's Dilemma strategies". Available at:
[arXiv:2001.05911](https://arxiv.org/abs/2001.05911)

## Software

To clone the repository locally run the following:

```
$ git clone https://github.com/Nikoleta-v3/meta-analysis-of-prisoners-dilemma-tournaments.git
```

A conda environment specifying all versions of libraries used is given in
`environment.yml`. To create and activate this environment run:

```
$ conda env create -f environment.yml
$ source activate axlml
```

## Reproducing the results

The raw data containing the summary results of each seeded tournament of each
type is achieved at: https://zenodo.org/record/3753498

To download and unpack the archived data run the following command whilst the
conda environment is activated:

```
$ inv data
```

To process the raw data run the following command (this takes some time):

```
$ inv process
```

This creates four data sets in the folder `data`:

- standard_3_processed.csv
- noise_3_processed.csv
- probend_3_processed.csv
- noise_probend_3_processed.csv

These are the data sets used to carry out the analysis of the paper.

There are also available to download here: https://zenodo.org/record/3753565 without carrying
out the process task.

The processed data sets can be downloaded by running the command:

```
$ inv prodata
```

## Analysis

The entire analysis presented in the paper is carried out in the Jupyter notebooks
under the `nbs/` folder.

The regression and correlation analysis is carried out for the merged data set
by running the scipts respectivaly:

```
$
$
```

The clustering analysis presented in the Appendix is performed using the script:

```
$
$
```

## Tests

Several scripts have been tested with `pytest`. To test run:

```
$ inv test
```

The software is released under an MIT license.
