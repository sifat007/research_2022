import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv ('list_conflict_events.csv')

print(df[-30:].to_string())
print(df.shape)
quit()
# print the column names
print (df.columns)

# only select relevant columns
process_df= (df[[
       'event_date', 'year', 'event_type', 'sub_event_type',
       'actor1', 'assoc_actor_1','actor2', 'assoc_actor_2', 'location',
       'source', 'source_scale', 'fatalities']])


# drop the first row ; it contains some irrevant flag strings
process_df= process_df.drop([0])  
print(process_df.location.value_counts())
print(process_df.event_type.value_counts())

# convert fatalities column into numeric
process_df["fatalities"] = pd.to_numeric(process_df["fatalities"]) 

#cond = process_df["location"].str.contains("Dhaka")
#process_df = process_df[cond] 

#cond = process_df["event_type"] == "Riots"
#process_df = process_df[cond] 

process_df['event_date']=process_df['event_date'].str[:7]

new_table = []
for year in range(2010, 2021):
       for month in range(1, 13):
              gen_date =str(year)+"-"+str(month).zfill(2)
              count = len(process_df[process_df.event_date == gen_date])
              fatatility_count = process_df[process_df.event_date == gen_date]['fatalities'].sum()
              row = {'month': gen_date, 'conflict_count': count, 'fatalities' : fatatility_count}
              new_table.append(row)
       #
#
print(pd.DataFrame(new_table))

# Save the preprocessed file
new_df =pd.DataFrame(new_table) 
new_df["month"] = pd.to_datetime(new_df["month"]) 
new_df.to_csv('processed_conflict_events.csv') 

# plot the dataframe
# formatting x axis labels
plt.rcParams.update({'font.size': 12})
plt.plot(new_df['month'], new_df['conflict_count'])
plt.title("Number of conflict events per month")
plt.xlabel("Year")
plt.ylabel("Number of conflicts")
plt.show()
 
