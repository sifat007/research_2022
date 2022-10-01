from __future__ import with_statement
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta


df = pd.read_csv ('wfp_food_prices_bgd.csv')

#index_df = pd.read_csv ('PFOODINDEXM.csv')
#index_df['PFOODINDEXM']= index_df['PFOODINDEXM']/100

# we have index value at 1st of each month
# to derive index value at 15th of each month we do,
# index value at 15th of N month = (index value at 1st of N month + index value at 1st of (N+1) month) / 2

#index_df["DATE"] = pd.to_datetime(index_df["DATE"]) 
#index_df["PFOODINDEXM"] = pd.to_numeric(index_df["PFOODINDEXM"]) 
#for i in range(len(index_df)-1):
#       current_row = index_df.iloc[[i]]
#       next_row = index_df.iloc[[i+1]]
#       index_at_15 = (float(current_row['PFOODINDEXM']) + float(next_row['PFOODINDEXM']))/2
#       index_df.loc[[i],'PFOODINDEXM'] = index_at_15
#       index_df.loc[[i],'DATE'] = current_row['DATE'] + timedelta(days=14)
##
#
#print(index_df)



# print the column names
print (df.columns)

# only select relevant columns
process_df= (df[['date', 'admin1',  'market',
       'category', 'commodity', 'unit', 'priceflag', 'pricetype', 'currency',
       'price', 'usdprice']])

# drop the first row ; it contains some irrevant flag strings
process_df= process_df.drop([0])  


# convert price column into number 
process_df["price"] = pd.to_numeric(process_df["price"]) 

# convert date to datetime
process_df["date"] = pd.to_datetime(process_df["date"]) 

# Divide price by 100 when price is given for 100 KG
cond=process_df['unit'] == '100 KG'
process_df.loc[cond,'price']= process_df.loc[cond,'price']/100  

# Select price for only Wheat flour


#cond = process_df["commodity"] == "Wheat flour"
cond = process_df["commodity"].str.contains("Oil")
process_df = process_df[cond] 

# Select price for only Dhaka
#print (process_df.admin1.value_counts())
#cond = process_df["admin1"] == "Dhaka"
#process_df = process_df[cond]

# Select price only Retail
print (process_df.pricetype.value_counts())
cond = process_df["pricetype"] == "Retail"
process_df = process_df[cond]    

# Select price for dates after 2010
cond = (process_df['date'] >= '2010-01-01') & (process_df['date'] < '2021-01-01')
process_df = process_df[cond]
print (process_df.commodity.value_counts())
#quit()

process_df = process_df.groupby(['date'])['price'].mean().reset_index()




# normalize the prices by dividing by global food index
#process_df = process_df.merge(index_df,how='left', left_on='date', right_on='DATE')
#process_df.loc[cond,'price']= process_df.loc[cond,'price']/100  
print(process_df)


# Print the number of selected rows
print("Number of rows selected ", len(process_df))

# Save the preprocessed file
process_df.to_csv('processed_food_price.csv') 

# plot the dataframe
plt.rcParams.update({'font.size': 12})
#ax = plt.gca()
#ax.xaxis.set_major_locator(DayLocator(interval=12))
#plt.plot(process_df['date'], process_df['price']/process_df['PFOODINDEXM'], label='normalized')

print(process_df[:-1]['date'].shape)
quit()
plt.plot(process_df['date'], process_df['price'])
plt.title("Average retail price of 1L cooking oil")
plt.xlabel("Year")
plt.ylabel("Price")
#plt.legend()
plt.show()
 
