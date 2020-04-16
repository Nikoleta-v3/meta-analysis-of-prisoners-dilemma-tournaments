from invoke import task
import pandas as pd

@task
def unpack(c):
    """
    Unpack downloaded `tar.gz` file
    """
    c.run("tar -xzf raw_data.tar.gz --directory data")


@task
def get(c):
    """
    Download the data from the online archive
    """
    c.run(
        "wget https://zenodo.org/record/3753498/files/raw_data.tar.gz?download=1 -O raw_data.tar.gz"
    )


@task
def data(c):
    """
    Download and unpack data from online archive
    """
    print("Downloading data")
    get(c)
    print("Unpacking data")
    unpack(c)


@task
def process(c):
    """
    Process raw data
    """
    print("Prepare raw data")
    c.run("python src/prepare_data.py data/raw_data/ all 3")

    for data_type in ['standard', 'noise', 'probend', 'probend_noise']:
        print(f"Process {data_type} data set")
        c.run(f"python src/process_data.py data/{data_type}_3.csv")


@task
def prodata(c):
    """
    Download and unpack data from online archive
    """
    print("Downloading processed data")
    c.run(
        "wget https://zenodo.org/record/3753565/files/data.tar.gz?download=1 -O data.tar.gz"
    )
    print("Unpacking data")
    c.run("tar -xzf data.tar.gz")


@task
def test(c):
    """
    Test all packaged code and notebooks
    """
    c.run("pytest tests")


@task
def merge(c):
    dfs = []
    for name in ['standard', 'noise', 'probend', 'probend_noise']:
        df = pd.read_csv(f'data/{name}_3_processed.csv')

        dfs.append(df)
    df = pd.concat(dfs)
    df.reset_index(inplace=True)
    df.to_csv('data/merged_3_processed.csv')