import pandas as pd
import matplotlib.pyplot as plt
food_df = pd.read_csv ('processed_food_price.csv')
conflict_df = pd.read_csv ('processed_conflict_events.csv')
result=food_df['price'].corr(conflict_df['conflict_count'])
print (result)

plt.rcParams.update({'font.size': 12})
plt.scatter(conflict_df['conflict_count'],food_df['price'])
plt.title("Number of conflicts vs price of cooking oil")
plt.xlabel("Number of conflicts")
plt.ylabel("Price")
plt.show()