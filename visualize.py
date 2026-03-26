import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = sys.argv[1]
df = pd.read_csv(file_path)

# -------- Plot 1 --------
df[['NUMBER OF PERSONS INJURED', 'NUMBER OF PERSONS KILLED']].hist(figsize=(8,4))
plt.suptitle('Injured vs Killed Distribution')

# -------- Plot 2 --------
selected_cols = [
    'NUMBER OF PERSONS INJURED',
    'NUMBER OF PERSONS KILLED',
    'NUMBER OF PEDESTRIANS INJURED',
    'NUMBER OF PEDESTRIANS KILLED',
    'NUMBER OF CYCLIST INJURED',
    'NUMBER OF CYCLIST KILLED',
    'NUMBER OF MOTORIST INJURED',
    'NUMBER OF MOTORIST KILLED'
]

corr = df[selected_cols].corr()

plt.figure(figsize=(10,8))
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title('Correlation Between Injury & Fatality Metrics')

# -------- Plot 3 --------
borough_counts = df['BOROUGH'].value_counts()

plt.figure(figsize=(8,6))
sns.barplot(x=borough_counts.index, y=borough_counts.values)
plt.title('Number of Collisions per Borough')
plt.xlabel('Borough')
plt.ylabel('Count')

# -------- Save --------
plt.savefig("summary_plot.png")
plt.close()

print("summary_plot.png saved successfully")