import pandas as pd
from pathlib import Path
from multiprocessing.pool import ThreadPool


# from concurrent.futures import ProcessPoolExecutor
from typing import List, Union

max_workers = 1  # Number of CPUs to use in parallel processing

# The content of 'all_features' should be a list of path-like  objects pointing to csv files containing the
# DataFrames to  concatenate. It can also be a list of already loaded and stacked  DataFrames.


def get_all_features_list(path,filepattern):
    return list(Path(path).glob(filepattern))

def get_feature(afile: Path) -> pd.Series:
    """ Loads the content of a .csv or .parquet file into a DataFrame, then stacks it in a Series
    The name of the file, without its extension, is used as the name of the Series,
    and will become, after concatenation, the name of the column.
    """
    feature = pd.read_parquet(afile).stack()
    feature.name = afile.stem
    return feature


def get_duo(thelist: List[Union[pd.DataFrame, pd.Series]]) -> Union[pd.Series, List[pd.Series]]:
    """Yields a pair of elements from a given list, or one element if only one element is present."""
    if len(thelist) == 0:
        raise ValueError("No element to yield!")
    if len(thelist) < 2:
        return thelist[0]
    length = len(thelist)
    for j in range(0, length, 2):
        if j >= len(thelist):
            return
        if j == len(thelist) - 1:
            yield thelist[-1]
        else:
            duo = thelist[j : j + 2]
            yield duo


def concat(duo: Union[pd.DataFrame, Union[pd.DataFrame, pd.Series, Path], Path]) -> Union[pd.Series, pd.DataFrame]:
    """Expects a pd.DataFrame or a path or a list of 2 pd.Series and returns the dataframe or the the series contained
     in the path or the aggregation of two series."""
    if isinstance(duo, list):
        if isinstance(duo[0], Path):
            df0 = get_feature(duo[0])
            df1 = get_feature(duo[1])
        else:
            df0 = duo[0]
            df1 = duo[1]
        return pd.concat([df0, df1], axis=1)
    else:
        if isinstance(duo, Path):
            return get_feature(duo)
        else:
            return duo


def fast_concat(features: List[Path]) -> pd.DataFrame:
    while len(features) != 1:
       with ThreadPool(processes=max_workers) as pool:
            features = list(pool.map(concat, get_duo(features)))
    features = features[0]
    return features.loc[:, sorted(features.columns)]

