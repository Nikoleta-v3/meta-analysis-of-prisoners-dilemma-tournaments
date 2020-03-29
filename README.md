Properties of winning Iterated Prisoner's Dilemma strategies. A meta
tournament analysis.
--------------------------------------

**Authors**: @Nikoleta-v3 @drvinceknight @marcharper

This repository contains the source code and analysis for a paper titled:
"Properties of winning Iterated Prisoner's Dilemma strategies.". Available at:
[arXiv:2001.05911](https://arxiv.org/abs/2001.05911)


## Software

A conda environment specifying all versions of libraries used is given in
`environment.yml`. To create and activate this environment run:

```
$ conda env create -f environment.yml
$ source activate axlml
```

## Data

The data sets used in this work is available on: https://zenodo.org/record/3516652#.Xl_vKy2caMA.

After downloading extract the `zip` at the top level of this repository after you
have cloned it locally.

To clone the repository locally run:

```
$ git clone https://github.com/Nikoleta-v3/meta-analysis-of-prisoners-dilemma-tournaments.git
```

The entire analysis described in the paper can be found in `nbs/`.

## Tests

Several scripts have been tested with `pytest`. To test run:

```
$ pytest tests
```

The software is released under an MIT license.
