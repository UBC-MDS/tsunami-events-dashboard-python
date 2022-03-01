import pandas as pd

def read_data(path):
    """
    TODO: add docstring
    """

    if not path:
        raise ValueError("Path of raw data file is required")

    # TODO: additional path validation required

    return pd.read_csv(path, sep="\t")
