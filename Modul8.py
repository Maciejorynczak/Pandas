import pandas as pd

# 1 dane
df = pd.read_csv('C:/Users/macie/Downloads/fatal-police-shootings-data.csv')
df.head()

# 2 zamiana tabeli
pivot_table = df.pivot_table(
    values='id',
    index='race', 
    columns='signs_of_mental_illness', 
    aggfunc='count'
)
print(pivot_table)


# 3 % ofiar z oznakami choroby psychicznej
pivot_table['mental_illness_percentage'] = pivot_table[True] / (pivot_table[True] + pivot_table[False]) * 100

pivot_table.sort_values(by='mental_illness_percentage', ascending=False, inplace=True)
pivot_table

#4 dzień tyg.
df['date'] = pd.to_datetime(df['date'])

df['day_of_week'] = df['date'].dt.day_name()

day_counts = df['day_of_week'].value_counts().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
day_counts
print(df[['date', 'day_of_week']].head())

import matplotlib.pyplot as plt

# Wykres
day_counts.plot(kind='bar', color='skyblue')
plt.title('Number of Fatal Police Interventions by Day of the Week')
plt.ylabel('Number of Interventions')
plt.xlabel('Day of the Week')
plt.xticks(rotation=45)
plt.show()