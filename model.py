import datetime
from os import path
import pandas as pd
from sklearn.linear_model import ElasticNet
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split


DATA_PATH = './data'
DOLLAR_DATA_FILENAME = path.normpath(f'{DATA_PATH}/dollar.csv')
IBOVESPA_DATA_FILENAME = path.normpath(f'{DATA_PATH}/ibovespa.csv')
CDI_DATA_FILENAME = path.normpath(f'{DATA_PATH}/cdi.csv')


def to_timestamp(d):
    timestamp = datetime.datetime.strptime(d, '%Y-%m-%d').timestamp()
    return int(timestamp / 1000)


dollar = pd.read_csv(DOLLAR_DATA_FILENAME, names=['date', 'dollar'], skiprows=[0])
ibovespa = pd.read_csv(IBOVESPA_DATA_FILENAME, names=['date', 'ibovespa'], skiprows=[0])
cdi = pd.read_csv(CDI_DATA_FILENAME, names=['date', 'cdi', 'selic'], skiprows=[0])

print(dollar.head())
print(ibovespa.head())
print(cdi.head())

df = pd.merge(pd.merge(ibovespa, dollar, how='inner', on='date'), cdi, how='inner', on='date')
df.sort_values(by=['date'], inplace=True)
df['timestamp'] = df['date'].transform(to_timestamp)
print(df.head())


def get_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)

    model = ElasticNet()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print(r2_score(y_test, y_pred))
    return model


model_ibovespa, model_cdi = get_model(df[['timestamp', 'dollar']], df['ibovespa']), get_model(df[['timestamp', 'dollar']], df['cdi'])

latest_dollar = df['dollar'].iat[-1]
today = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
print('Predict:')
print('Based on latest dollar', latest_dollar, '\n')
print('Date\t\tIBOV\t\tCDI')
pred_single = lambda m, t: m.predict([[t, latest_dollar]])[0]
for i in range(0, 20):
    date = today + datetime.timedelta(days=i * 10)
    timestamp = today.timestamp()
    ibovespa_pred = pred_single(model_ibovespa, timestamp)
    cdi_pred = pred_single(model_cdi, timestamp)
    print(date.strftime('%Y-%m-%d'), ibovespa_pred, cdi_pred)


model = get_model(df[['timestamp', 'dollar', 'cdi']], df['ibovespa'])

latest = df['dollar'].iat[-1], df['cdi'].iat[-1]
today = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
print('Predict:')
print('Based on latest dollar and cdi', latest, '\n')
print('Date\t\tIBOV')
pred_single = lambda m, t: m.predict([[t, *latest]])[0]
for i in range(0, 20):
    date = today + datetime.timedelta(days=i * 10)
    timestamp = today.timestamp()
    pred = pred_single(model, timestamp)
    print(date.strftime('%Y-%m-%d'), pred)
