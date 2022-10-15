import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller
from statsmodels.stats.stattools import durbin_watson
from statsmodels.tsa.api import VAR
register_matplotlib_converters()

# 1. Load datasets
df_food = pd.read_csv('processed_food_price.csv', index_col=0, parse_dates=[0])
df_conflict = pd.read_csv('processed_conflict_events.csv', index_col=0, parse_dates=[0])

print(df_food.head())
print(df_conflict.head())

# 2. Merge the dataframes
df_food_conflict = df_food.merge(df_conflict.conflict_count, on='date')
print(df_food_conflict.head())

# Function to test stationarity
def perform_adf_test(name, series):
    result = adfuller(series)
    print("Results for Augmented Dicky-Fuller Test for checking stationarity for " + name) 
    print("---------------------------------------------------------------------")
    print('ADF Statistic: %f' % result[0])
    print('p-value: %f' % result[1])
    print("=====================================================================")
#

# 3. Test stationarity of the original time series
perform_adf_test("Rice", df_food_conflict.rice)
perform_adf_test("Oil", df_food_conflict.oil)
perform_adf_test("Wheat", df_food_conflict.wheat)
perform_adf_test("Conflict", df_food_conflict.conflict_count)

# Note: Can achieve stationarity without normalization. Skipping normalization.
#def normalize(df):
#    avg = df.mean()
#    stdev = df.std()
#    df = (df - avg) /stdev
##
# normalize the food dataframe
#normalize(df_food)


# 4. Split the dataset into train and test
TEST_SIZE = 5

df_food_conflict_train = df_food_conflict[:-TEST_SIZE]
df_food_conflict_test = df_food_conflict[-TEST_SIZE:]

# 5. Take the first difference of dataframe to achieve stationarity
df_differenced = df_food_conflict_train.diff().dropna()


# 6. Test stationarity of the differenced time series
perform_adf_test("Rice",df_differenced.rice)
perform_adf_test("Oil",df_differenced.oil)
perform_adf_test("Wheat",df_differenced.wheat)
perform_adf_test("Conflict", df_differenced.conflict_count)


# Function to plot the dataframe
def plot_dataframe(df):
    fig, axes = plt.subplots(nrows=2, ncols=2, dpi=120, figsize=(10,6))
    for i, ax in enumerate(axes.flatten()):
        data = df[df.columns[i]]
        ax.plot(data, color='red', linewidth=1)
        # Decorations
        ax.set_title(df.columns[i])
        ax.xaxis.set_ticks_position('none')
        ax.yaxis.set_ticks_position('none')
        #ax.tick_params(labelsize=6)
    #
    plt.tight_layout(); 
    #plt.show()
#

# Plot original dataframe
plot_dataframe(df_food_conflict)
# Plot differenced dataframe
plot_dataframe(df_differenced)

# 7. Create the VAR model
model = VAR(df_differenced)

# 8. Fit the VAR model
MAX_LAG=13
model_fit = model.fit(maxlags=MAX_LAG)

# 9. Print summary of the VAR model
print(model_fit.summary())

# 10. Run Durbin Watson test to make sure that there are no leftover pattern that were not captured by the VAR model
print("Check for left overpattern in the residual(error) using Durbin Watson function: ")
print(durbin_watson(model_fit.resid))
print("=============================================================\n\n")

# 11. Calculate FEVD (Forcast Error Variance Decomposition)
fevd = model_fit.fevd(MAX_LAG)
fevd.summary()
fevd.plot()

# 12. Plot the residuals(errors) of VAR
plot_dataframe(model_fit.resid)

# 13. Forecast
forecast_input = df_differenced.values[-MAX_LAG:]
fc = model_fit.forecast(y=forecast_input, steps=TEST_SIZE)
df_forecast = pd.DataFrame(fc, index=df_food_conflict_test.index, columns=df_food_conflict_test.columns)
print(df_forecast)

# NOTE: becase we trained the model with first diff data, the forcast is in first diff
# 14. Revert first diff of the forcast
df_forecast_actual = df_food_conflict_train.iloc[-1] + df_forecast.cumsum()
print(df_forecast)
print(df_forecast_actual)
print(df_food_conflict_test)

# 15. Plot forcasted vs actual conflict events
plt.figure(figsize=(10,6))
plt.title("Forcasting Conflict Events")
plt.plot(df_forecast_actual.conflict_count, label="forcast")
plt.plot(df_food_conflict.conflict_count, label="original")
plt.legend()
plt.show()
