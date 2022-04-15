import pandas as pd
from data import DATA_FILENAME, load_model_config
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split, cross_val_score, ShuffleSplit


RANDOM_SEED = 42  # Constant integer value for the random state params

df = pd.read_csv(DATA_FILENAME)
config = load_model_config()
y_col, X_cols = config['y'], config['X']

X, y = df[X_cols], df[y_col]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=RANDOM_SEED, shuffle=True)


def plot_results(title, y_pred):
    _len = len(X_cols)
    fig, sub_plts = plt.subplots(_len, 1)
    fig.text(0.5, 0.95, title, ha='center', va='top', rotation='horizontal', fontweight='bold')
    for i in range(0, _len):
        col = X_cols[i]
        ax = sub_plts if _len == 1 else sub_plts[i]
        ax.scatter(X_test[col], y_test, color="black", label='Real')
        ax.scatter(X_test[col], y_pred, color="blue", label='Pred')
        ax.legend()
        ax.set_title(col)

    fig.text(0.07, 0.5, y_col, ha='center', va='center', rotation='vertical')
    plt.subplots_adjust(wspace=0, hspace=0.25)
    fig.set_size_inches(10, 10)
    plt.show()


def test_model(model, X, y, y_pred, y_test, title=None):
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    print(f'{type(model).__name__ if title is None else title}:\n\tr2_score: {r2}\n\tmean_absolute_error: {mae}')
    cv_scores = cross_val_score(model, X, y, cv=ShuffleSplit(n_splits=5, test_size=0.5, random_state=RANDOM_SEED))
    mean, std = cv_scores.mean(), cv_scores.std()
    print("\tcross validation: %0.2f accuracy with a standard deviation of %0.6f" %
          (mean, std), f'and values {cv_scores}')
    return mean


def test_columns(model, cv_score):
    best_model = None
    X_cols = X_train.columns
    _len = len(X_cols)
    title = type(model).__name__
    fig, sub_plts = plt.subplots(_len, 1)
    for i in range(0, _len):
        col = X_cols[i]
        subtitle = f'{title} {col}'
        X_train_, X_test_ = X_train[[col]], X_test[[col]]
        model.fit(X_train_, y_train)
        y_pred = model.predict(X_test_)

        ax = sub_plts if _len == 1 else sub_plts[i]
        ax.scatter(X_test_[col], y_test, color="black", label='Real')
        ax.scatter(X_test_[col], y_pred, color="blue", label='Pred')
        ax.legend()
        ax.set_title(subtitle)

        cv_score_ = test_model(model, X[[col]], y, y_pred, y_test, title=subtitle)
        if cv_score_ > cv_score:
            cv_score = cv_score_
            best_model = model
        
    fig.text(0.07, 0.5, y_col, ha='center', va='center', rotation='vertical')
    plt.subplots_adjust(wspace=0, hspace=0.25)
    fig.set_size_inches(10, 10)
    plt.show()
    return best_model


linear_model = LinearRegression()
linear_model.fit(X_train, y_train)
linear_model_y_pred = linear_model.predict(X_test)
print(
    f'LinearRegression: Coefficients {linear_model.coef_}  Intercept {linear_model.intercept_}')
cv_score = test_model(linear_model, X, y, linear_model_y_pred, y_test)
plot_results('LinearRegression', linear_model_y_pred)
linear_model = test_columns(LinearRegression(), cv_score) or linear_model

svr_model = SVR()
svr_model.fit(X_train, y_train)
svr_model_y_pred = svr_model.predict(X_test)
cv_score = test_model(svr_model, X, y, svr_model_y_pred, y_test)
plot_results('SVR', svr_model_y_pred)
svr_model = test_columns(SVR(), cv_score) or svr_model

random_forest_model = RandomForestRegressor(max_leaf_nodes=5, random_state=RANDOM_SEED)
random_forest_model.fit(X_train, y_train)
random_forest_model_y_pred = random_forest_model.predict(X_test)
cv_score = test_model(random_forest_model, X, y, random_forest_model_y_pred, y_test)
plot_results('RandomForestRegressor', random_forest_model_y_pred)
random_forest_model = test_columns(RandomForestRegressor(max_leaf_nodes=5, random_state=RANDOM_SEED), cv_score) or random_forest_model

random_forest_model2 = RandomForestRegressor(max_leaf_nodes=None, random_state=RANDOM_SEED)
random_forest_model2.fit(X_train, y_train)
random_forest_model2_y_pred = random_forest_model2.predict(X_test)
cv_score = test_model(random_forest_model2, X, y, random_forest_model2_y_pred, y_test)
plot_results('RandomForestRegressor (Unlimited leaf nodes)', random_forest_model2_y_pred)
random_forest_model2 = test_columns(RandomForestRegressor(max_leaf_nodes=None, random_state=RANDOM_SEED), cv_score) or random_forest_model2


# # save the model

import pickle

f = open('svr_model.bin', 'wb')
pickle.dump(svr_model, f)
f.close()
