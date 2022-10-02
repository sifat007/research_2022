from numpy import squeeze
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.api import VAR
from scipy.stats import pearsonr
register_matplotlib_converters()

df_food = pd.read_csv('processed_food_price.csv', index_col=0, parse_dates=[0])

print(df_food.head())


# normalize the series
avg = df_food.mean()
stdev = df_food.std()
#df_food = (df_food - avg) /stdev

# take the first diff
#df_food = df_food.diff().dropna()


def test_series(name, x):
    plt.figure(figsize=(10,4))
    plt.plot(x)
    plt.title(name, fontsize=20)
    plt.ylabel('Price', fontsize=16)

    plot_acf(x, lags=12)
    plot_pacf(x)

    def perform_adf_test(series):
        result = adfuller(series)
        print('ADF Statistic: %f' % result[0])
        print('p-value: %f' % result[1])
    #

    perform_adf_test(x)
    #plt.show()
#


#test_series("Rice",df_food.rice)
#test_series("Oil",df_food.oil)
#test_series("Wheat",df_food.wheat)

df_food = df_food[['rice', 'oil','wheat']]
print(df_food)

model = VAR(df_food)

model_fit = model.fit(maxlags=13)

print(model_fit.summary())
model_fit.plot()
model_fit.plot_acorr()
model_fit.irf(10).plot(orth=False)
print(model_fit.test_causality('rice',['oil', 'wheat'], kind='f'))
plt.show()
