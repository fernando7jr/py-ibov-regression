import pandas as pd
from data import DATA_FILENAME, load_model_config
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split, cross_val_score, ShuffleSplit


RANDOM_SEED = 42  # Constant integer value for the random state params

df = pd.read_csv(DATA_FILENAME)
config = load_model_config()
y_col, X_cols = config['y'], config['X']
X, y = df[X_cols], df[y_col]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=RANDOM_SEED, shuffle=True)


def plot_results(y_pred):
    fig, sub_plts = plt.subplots(3, 1)
    for i in range(0, 3):
        col = X_cols[i]
        ax = sub_plts[i]
        ax.scatter(X_test[col], y_test, color="black", label='Real')
        ax.scatter(X_test[col], y_pred, color="blue", label='Pred')
        ax.legend()
        ax.set_title(col)

    fig.text(0.07, 0.5, y_col, ha='center', va='center', rotation='vertical')
    plt.subplots_adjust(wspace=0, hspace=0.25)
    fig.set_size_inches(10, 10)
    plt.show()


def test_model(model, y_pred):
    r2 = r2_score(y_test, y_pred)
    print(f'{type(model).__name__}:\n\tr2_score: {r2}')
    cv_scores = cross_val_score(model, X, y, cv=ShuffleSplit(n_splits=5, test_size=0.5, random_state=RANDOM_SEED))
    print("\tcross validation: %0.2f accuracy with a standard deviation of %0.6f" %
          (cv_scores.mean(), cv_scores.std()), f'and values {cv_scores}')


linear_model = LinearRegression()
linear_model.fit(X_train, y_train)
linear_model_y_pred = linear_model.predict(X_test)
print(
    f'LinearRegression: Coefficients {linear_model.coef_}  Intercept {linear_model.intercept_}')
test_model(linear_model, linear_model_y_pred)
plot_results(linear_model_y_pred)

svr_model = SVR()
svr_model.fit(X_train, y_train)
svr_model_y_pred = svr_model.predict(X_test)
test_model(svr_model, svr_model_y_pred)
plot_results(svr_model_y_pred)

random_forest_model = RandomForestRegressor(max_leaf_nodes=5, random_state=RANDOM_SEED)
random_forest_model.fit(X_train, y_train)
random_forest_model_y_pred = random_forest_model.predict(X_test)
test_model(random_forest_model, random_forest_model_y_pred)
plot_results(random_forest_model_y_pred)

random_forest_model2 = RandomForestRegressor(max_leaf_nodes=None, random_state=RANDOM_SEED)
random_forest_model2.fit(X_train, y_train)
random_forest_model2_y_pred = random_forest_model2.predict(X_test)
test_model(random_forest_model2, random_forest_model2_y_pred)
plot_results(random_forest_model2_y_pred)

