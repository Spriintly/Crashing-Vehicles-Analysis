import sys
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = sys.argv[1]
df = pd.read_csv(file_path)

# clean columns
df.columns = df.columns.str.strip().str.lower()


fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Plot 1 
axes[0].hist(df['number_of_persons_injured'], bins=20, alpha=0.6, label='Injured')
axes[0].hist(df['number_of_persons_killed'], bins=20, alpha=0.6, label='Killed')
axes[0].set_title('Injured vs Killed Distribution')
axes[0].legend()

#  Plot 2 
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
sns.heatmap(corr, annot=True, cmap='coolwarm', ax=axes[1])
axes[1].set_title('Correlation Between Injury & Fatality Metrics')

# Plot 3 
borough_counts = df['borough'].value_counts()
sns.barplot(x=borough_counts.index, y=borough_counts.values, ax=axes[2])

axes[2].set_title('Number of Collisions per Borough')
axes[2].set_xlabel('Borough')
axes[2].set_ylabel('Count')

#  Save 
plt.tight_layout()
plt.savefig("summary_plot.png")
plt.close()

print("summary_plot.png saved")

# Call next script
subprocess.run(["python", "cluster.py", file_path])