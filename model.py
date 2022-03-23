import pandas as pd
from data import DATA_FILENAME, load_model_config
from sklearn.linear_model import ElasticNet
from sklearn.svm import SVR
from sklearn.ensemble import AdaBoostRegressor
from sklearn.metrics import r2_score, explained_variance_score
from sklearn.model_selection import train_test_split


RANDOM_STATE = 42


def test_model(model):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    r2, variance = r2_score(y_pred, y_test), explained_variance_score(y_pred, y_test)
    print(type(model).__name__, f'r2_score: {r2}\texplained_variance_score: {variance}')
    return y_pred


df = pd.read_csv(DATA_FILENAME)
config = load_model_config()
y_col, X_cols = config['y'], config['X']

X_train, X_test, y_train, y_test = train_test_split(df[X_cols], df[y_col], test_size=0.33, random_state=RANDOM_STATE, shuffle=True)

test_model(ElasticNet(random_state=RANDOM_STATE))
test_model(SVR(random_state=RANDOM_STATE))
test_model(AdaBoostRegressor(random_state=RANDOM_STATE))
