import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

file_path = "C:/Users/macie/Downloads/HRDataset.csv"
hr_data = pd.read_csv(file_path)

hr_data['DateofHire'] = pd.to_datetime(hr_data['DateofHire'], errors='coerce')
hr_data['DateofTermination'] = pd.to_datetime(hr_data['DateofTermination'], errors='coerce')
hr_data['DOB'] = pd.to_datetime(hr_data['DOB'], errors='coerce')

hr_data['Age'] = (pd.Timestamp("now") - hr_data['DOB']).dt.days / 365


#Zadanie 1
plt.figure(figsize=(12, 8))
sns.boxplot(x='ManagerName', y='PerformanceScore', data=hr_data)
plt.xticks(rotation=90)
plt.title('Performance Score by Manager')
plt.show()
print(hr_data.head())