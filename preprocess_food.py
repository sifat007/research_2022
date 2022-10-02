from __future__ import with_statement
from cProfile import label
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta

df = pd.read_csv ('wfp_food_prices_bgd.csv')


# only select relevant columns
process_df= (df[['date', 'admin1',  'market',
       'category', 'commodity', 'unit', 'priceflag', 'pricetype', 'currency',
       'price', 'usdprice']])

# drop the first row ; it contains some irrevant flag strings
process_df = process_df.drop([0]) 

# convert price column into number 
process_df["price"] = pd.to_numeric(process_df["price"]) 

# convert date to datetime
process_df["date"] = pd.to_datetime(process_df["date"]) 

# Divide price by 100 when price is given for 100 KG
cond=process_df['unit'] == '100 KG'
process_df.loc[cond,'price']= process_df.loc[cond,'price']/100  

# Select price only Retail
print (process_df.pricetype.value_counts())
cond = process_df["pricetype"] == "Retail"
process_df = process_df[cond]    

# Select price for dates after 2010
cond = (process_df['date'] >= '2010-01-01') & (process_df['date'] < '2020-12-01')
process_df = process_df[cond]

# TODO: Select price for only Dhaka
#print (process_df.admin1.value_counts())
#cond = process_df["admin1"] == "Dhaka"
#process_df = process_df[cond]

# Select price for only Wheat flour

cond = process_df["commodity"].str.contains("Oil")
df_oil = process_df[cond] 
df_oil = df_oil.groupby(['date'])['price'].mean().reset_index().rename(columns={'price':'oil'})

cond = process_df["commodity"] == "Wheat flour"
df_wheat = process_df[cond] 
df_wheat = df_wheat.groupby(['date'])['price'].mean().reset_index().rename(columns={'price':'wheat'})

cond2 =  process_df["commodity"].str.contains("Rice")
cond1 = process_df["commodity"].str.contains("coarse")
df_rice = process_df[cond1 & cond2] 
df_rice = df_rice.groupby(['date'])['price'].mean().reset_index().rename(columns={'price':'rice'})
print(len(df_rice))

df_combined = df_rice.merge(df_wheat, on='date').merge(df_oil, on='date')
df_combined.set_index('date', inplace=True)
print(df_combined)



# normalize the prices by dividing by global food index
#process_df = process_df.merge(index_df,how='left', left_on='date', right_on='DATE')
#process_df.loc[cond,'price']= process_df.loc[cond,'price']/100  
#print(process_df)


# Print the number of selected rows
print("Number of rows selected ", len(df_combined))

# Save the preprocessed file
df_combined.to_csv('processed_food_price.csv') 

# plot the dataframe
plt.rcParams.update({'font.size': 12})
plt.plot(df_combined.rice, label="rice")
plt.plot(df_combined.wheat, label="wheat")
plt.plot(df_combined.oil, label="oil")
plt.legend()
plt.title("Average retail price of different commodities")
plt.xlabel("Year")
plt.ylabel("Price in BDT")
#plt.legend()
plt.show()
 
