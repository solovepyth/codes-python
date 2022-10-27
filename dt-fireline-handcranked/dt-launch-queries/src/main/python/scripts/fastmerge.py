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

def get_filefeature(afile: Path) -> pd.DataFrame:
    """ Loads the content of a .csv or .parquet file into a DataFrame, then stacks it in a Series
    The name of the file, without its extension, is used as the name of the Series,
    and will become, after concatenation, the name of the column.
    """
    feature = pd.read_parquet(afile)
    feature.columns=[*feature.columns[:-1], afile.stem]
    print(f"{afile.stem} : {feature.shape[0]} lignes extraites - aperçu : {feature.head(5)}")
    return feature


def get_duo(thelist: List[Union[pd.DataFrame, Path]]) -> Union[pd.DataFrame, List[pd.DataFrame]]:
    """Yields a pair of elements from a given list, or one element if only one element is present."""
    if len(thelist) == 0:
        raise ValueError("No element to yield!")
    if len(thelist) < 2:
        print(f"duo :{thelist[0]}")
        return thelist[0]
    length = len(thelist)
    for j in range(0, length, 2):
        if j >= len(thelist):
            return
        if j == len(thelist) - 1:
            print(f"duo :{thelist[-1]}")
            yield thelist[-1]
        else:
            duo = thelist[j : j + 2]
            print(f"duo :{duo}")
            yield duo


def merge(duo: Union[pd.DataFrame, Union[pd.DataFrame, Path], Path]) -> pd.DataFrame:
    """Expects a pd.DataFrame or a path or a list of 2 pd.Series and returns the dataframe or the the series contained
     in the path or the aggregation of two series."""
    if isinstance(duo, list):
        if isinstance(duo[0], Path):
            df0 = get_filefeature(duo[0])
            df1 = get_filefeature(duo[1])
            lstmerge=[x for x in df0.columns if x not in  df0.columns.tolist()[-1:]]
        else:
            df0 = duo[0]
            df1 = duo[1]
            lstmerge=[x for x in df0.columns.tolist() if x in df1.columns.tolist()]
        print(f"lstmerge : {lstmerge}")
        df_final=pd.merge(df0, df1, how="outer",on=lstmerge)
        lstnacols=[x for x in df_final.columns.tolist() if x not in lstmerge]
        df_final[lstnacols]=df_final[lstnacols].fillna(value=0)
        print(f"df_final : {df_final.head(5)} - {df_final.shape[0]} lignes")
        return df_final
    else:
        if isinstance(duo, Path):
            print(f"get_filefeature(duo) : {get_filefeature(duo).head(5)}")
            return get_filefeature(duo)
        else:
            print(f"duo : {duo.head(5)}")
            return duo


def fast_merge(features: List[Path]) -> pd.DataFrame:
    while len(features) != 1:
       with ThreadPool(processes=max_workers) as pool:
            features = list(pool.map(merge, get_duo(features)))            
    features = features[0]
    return features.loc[:, sorted(features.columns)]
