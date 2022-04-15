import pandas as pd
from data import DATA_FILENAME
import matplotlib.pyplot as plt

df = pd.read_csv(DATA_FILENAME).set_index('days_since_1998')
print('Describe')
print(df[['ibovespa', 'dollar', 'cdi']].describe())
print('Correlation')
print(df[['ibovespa', 'dollar', 'cdi']].corr())

df[['ibovespa', 'dollar', 'cdi']].plot(subplots=True, layout=(3,1), figsize=(7,7))
plt.show()

df2 = df[df.index >= 4000]
print('Correlation')
print(df2[['ibovespa', 'dollar', 'cdi']].corr())

df2[['ibovespa', 'dollar', 'cdi']].plot(subplots=True, layout=(3,1), figsize=(7,7))
plt.show()

print('Describe')
print(df2[['ibovespa_norm', 'dollar_norm', 'cdi_norm']].describe())
print('Correlation')
print(df2[['ibovespa_norm', 'dollar_norm', 'cdi_norm']].corr())

df2[['ibovespa_norm', 'dollar_norm', 'cdi_norm']].plot(subplots=True, layout=(3,1), figsize=(7,7))
plt.show()

print('Describe')
print(df2[['ibovespa', 'dollar', 'cdi', 'ibovespa_%', 'dollar_%', 'cdi_%']].describe())
print('Correlation')
print(df2[['ibovespa', 'dollar', 'cdi', 'ibovespa_%', 'dollar_%', 'cdi_%']].corr())

df2[['ibovespa_%', 'dollar_%', 'cdi_%']].plot(subplots=True, layout=(3,1), figsize=(7,7))
plt.show()
