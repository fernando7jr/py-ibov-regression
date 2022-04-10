from . import save_cdi_data, save_dollar_data, save_index_data, SAVE_DIR, DATA_FILENAME, MODEL_CONFIG_FILENAME, path


import datetime
import json
import pandas as pd
from csv import QUOTE_NONNUMERIC
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import SelectKBest, f_regression


BASE_DATE = datetime.date(1998, 1, 1)

def to_days_since_1998(d):
    delta = datetime.date.fromisoformat(d) - BASE_DATE
    return delta.days


def __get_filename(outfilename, func):
    _path = path.join(SAVE_DIR, outfilename)
    if path.isfile(_path) is False:
        return func(outdir=SAVE_DIR, outfilename=outfilename)
    return _path


def get_cdi_data():
    return pd.read_csv(__get_filename('cdi.csv', save_cdi_data), names=['date', 'cdi'], skiprows=[0])


def get_dollar_data():
    return pd.read_csv(__get_filename('dollar.csv', save_dollar_data), names=['date', 'dollar'], skiprows=[0])


def get_ibovespa_data():
    return pd.read_csv(__get_filename('ibovespa.csv', save_index_data), names=['date', 'ibovespa'], skiprows=[0])


if __name__ == '__main__' or not path.isfile(DATA_FILENAME):
    # load all data
    cdi = get_cdi_data()
    dollar = get_dollar_data()
    ibovespa = get_ibovespa_data()

    # merge into a single data frame
    df = pd.merge(pd.merge(ibovespa, dollar, how='inner',
                  on='date'), cdi, how='inner', on='date')
    df.sort_values(by=['date'], inplace=True)
    df['days_since_1998'] = df['date'].transform(to_days_since_1998)
    print('Data')
    print(df.shape)
    print(df.head())
    print('Number of duplicated lines', df['date'].duplicated().sum())
    print('Number of null values', df.isnull().sum().sum())
    
    COLUMNS = ['cdi', 'dollar', 'ibovespa']
    # apply normalization to the columns
    for col in COLUMNS:
        min_max_scaler = MinMaxScaler()
        result = min_max_scaler.fit_transform(df[[col]])
        df[f'{col}_norm'] = result[:, 0]
    print('After normalization')
    print(df.shape)
    print(df.head())

    # create new columns for the fluctuation percentage
    for col in COLUMNS:
        df[f'{col}_%'] = df[col].pct_change().fillna(0)
    print('After calculating fluctuation percentage')
    print(df.shape)
    print(df.head())

    # export to a new csv file
    df.to_csv(
        DATA_FILENAME,
        decimal='.',
        sep=',',
        index=False,
        quoting=QUOTE_NONNUMERIC
    )

    # create a new df using feature selection to choose the most relevant columns
    SELECTABLE_COLUMNS = ['dollar_norm', 'cdi_norm', 'dollar_%', 'cdi_%', 'days_since_1998']
    TARGET_COLUMN = 'ibovespa_norm'
    K = 3
    X, y = df[SELECTABLE_COLUMNS], df[TARGET_COLUMN]
    select_k_best = SelectKBest(f_regression, k=K)
    select_k_best.fit(X, y)

    # identify the columns by the index
    selected_cols_ids = select_k_best.get_support(indices=True)
    selected_cols_scores = list(map(lambda i: select_k_best.scores_[i], selected_cols_ids))
    selected_cols = list(map(lambda i: SELECTABLE_COLUMNS[i], selected_cols_ids))

    # save to a json file
    with open(MODEL_CONFIG_FILENAME, 'wt') as f:
        json.dump({'y': TARGET_COLUMN, 'X': selected_cols, 'scores': selected_cols_scores, 'k': K}, f)
