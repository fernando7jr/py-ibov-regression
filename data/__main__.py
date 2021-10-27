from . import save_cdi_data, save_dollar_data, save_index_data, SAVE_DIR, DATA_FILENAME, path


import datetime
import pandas as pd
from csv import QUOTE_NONNUMERIC
from sklearn.preprocessing import MinMaxScaler


ONE_DAY_IN_SECONDS = 3600 * 24

def to_timestamp(d):
    timestamp = datetime.datetime.strptime(d, '%Y-%m-%d').timestamp()
    return int(timestamp / ONE_DAY_IN_SECONDS)


def __get_filename(outfilename, func):
    _path = path.join(SAVE_DIR, outfilename)
    if path.isfile(_path) is False:
        return func(outdir=SAVE_DIR, outfilename=outfilename)
    return _path


def get_cdi_data():
    return pd.read_csv(__get_filename('cdi.csv', save_cdi_data), names=['date', 'cdi', 'selic'], skiprows=[0])


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
    df['timestamp'] = df['date'].transform(to_timestamp)
    print('Data')
    print(df.shape)
    print(df.head())
    print('Number of duplicated lines', df['date'].duplicated().sum())
    print('Number of null values', df.isnull().sum().sum())
    
    COLUMNS = ['cdi', 'selic', 'dollar', 'ibovespa']
    # apply normalization to the columns
    for col in COLUMNS:
        min_max_scaler = MinMaxScaler()
        result = min_max_scaler.fit_transform(df[[col]])
        df[f'{col}_norm'] = result[:, 0]
    print('After normalization')
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
    
