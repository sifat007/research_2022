from matplotlib import test
from numpy import squeeze
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller
from statsmodels.stats.stattools import durbin_watson
from statsmodels.tsa.api import VAR
from scipy.stats import pearsonr
register_matplotlib_converters()

df_food = pd.read_csv('processed_food_price.csv', index_col=0, parse_dates=[0])
df_conflict = pd.read_csv('processed_conflict_events.csv', index_col=0, parse_dates=[0])

print(df_food.head())
print(df_conflict.head())



def normalize(df):
    avg = df.mean()
    stdev = df.std()
    df = (df - avg) /stdev
#

# normalize the food dataframe
#normalize(df_food)
# take the first diff of food dataframe
#df_food = df_food.diff().dropna()

# normalize the conflict dataframe
#normalize(df_conflict)
# take the first diff of the conflict dataframe 
#df_conflict = df_conflict.diff().dropna()





def test_series(name, df):
    plt.figure(figsize=(10,4))
    plt.plot(df)
    plt.title(name, fontsize=20)
    plt.ylabel('Price', fontsize=16)

    #plot_acf(df, lags=12)
    #plot_pacf(df)

    def perform_adf_test(series):
        result = adfuller(series)
        print('ADF Statistic: %f' % result[0])
        print('p-value: %f' % result[1])
    #

    perform_adf_test(df)
    plt.show()
#

#test_series("Conflict", df_conflict.conflict_count)
#
#test_series("Rice",df_food.rice)
#test_series("Oil",df_food.oil)
#test_series("Wheat",df_food.wheat)



df_food = df_food[['rice', 'oil','wheat']]
df_food_conflict = df_food.merge(df_conflict.conflict_count, on='date')
print(df_food_conflict.head())

model = VAR(df_food_conflict)

model_fit = model.fit(maxlags=13)

print(model_fit.summary())

print("Check for left overpattern in the residual(error) using Durbin Watson function: ")
print(durbin_watson(model_fit.resid))
print("=============================================================\n\n")

model_fit.plot()
#model_fit.plot_acorr()
fevd = model_fit.fevd(13)
fevd.summary()
fevd.plot()
plt.show()
