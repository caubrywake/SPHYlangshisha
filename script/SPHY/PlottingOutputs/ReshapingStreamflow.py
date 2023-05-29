# -*- coding: utf-8 -*-
"""
reshaping streamflow data
for karnali for pranisha
"""
'H:\upto2008.xlsx'


import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('H:/testyear.csv')


import pandas as pd

# Create a sample DataFrame with numbered columns
df = pd.DataFrame({'1': [1, 2, 3],
                   '2': [4, 5, 6],
                   '3': [7, 8, 9],
                   '4': [10, 11, 12],
                   '5': [13, 14, 15],
                   '6': [16, 17, 18],
                   '7': [19, 20, 21],
                   '8': [22, 23, 24],
                   '9': [25, 26, 27],
                   '10': [28, 29, 30],
                   '11': [31, 32, 33],
                   '12': [34, 35, 36]})

# Reshape the DataFrame from wide to long format
df_long = pd.melt(df, value_vars=[str(i) for i in range(1, 13)], var_name='variable', value_name='value')

# Convert the 'variable' column to integer type
df_long['variable'] = df_long['variable'].astype(int)

# Sort the DataFrame by 'variable' column
df_long.sort_values('variable', inplace=True)

# Reset the index
df_long.reset_index(drop=True, inplace=True)

print(df_long)









# Check the current shape of the DataFrame
print("Original shape:")
print(df.shape)

# Reshape the DataFrame from wide to long format
df = pd.melt(df, id_vars='Year', value_vars=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
              var_name='Month', value_name='Value')

# Drop rows with missing values in 'Value' column
df.dropna(subset=['Value'], inplace=True)

# Convert 'Year' and 'Month' columns to integers
df['Year'] = df['Year'].astype(int)
df['Month'] = df['Month'].astype(int)

# Create a datetime column combining 'Year' and 'Month'
df['Month'] = pd.to_datetime(df[['Year', 'Month']].assign(day=1))

# Set 'Month' as the index
df.set_index('Month', inplace=True)

# Drop 'Year' and 'Month' columns
df.drop(['Year', 'Month'], axis=1, inplace=True)

# Check the reshaped shape of the DataFrame
print("\nReshaped shape:")
print(df.shape)

# Preview the reshaped DataFrame
print("\nPreview of reshaped DataFrame:")
print(df.head())




