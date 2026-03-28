import sys
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = sys.argv[1]
df = pd.read_csv(file_path)

# clean columns
df.columns = df.columns.str.strip().str.lower()

#Plot 1
df[['number_of_persons_injured', 'number_of_persons_killed']].hist(figsize=(8,4))
plt.suptitle('Injured vs Killed Distribution')

#Plot 2
selected_cols = [
    'number_of_persons_injured',
    'number_of_persons_killed',
    'number_of_pedestrians_injured',
    'number_of_pedestrians_killed',
    'number_of_cyclist_injured',
    'number_of_cyclist_killed',
    'number_of_motorist_injured',
    'number_of_motorist_killed'
]

corr = df[selected_cols].corr()

plt.figure(figsize=(10,8))
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title('Correlation Between Injury & Fatality Metrics')

#Plot 3 
plt.figure(figsize=(8,6))
borough_counts = df['borough'].value_counts()

sns.barplot(x=borough_counts.index, y=borough_counts.values)

plt.title('Number of Collisions per Borough')
plt.xlabel('Borough')
plt.ylabel('Count')

#Save 
plt.savefig("summary_plot.png")
plt.close()

print("summary_plot.png saved")

# Call next script
subprocess.run(["python", "cluster.py", file_path])