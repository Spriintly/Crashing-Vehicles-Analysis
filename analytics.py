import sys
import pandas as pd
import subprocess

input_path = sys.argv[1]
df = pd.read_csv(input_path)

# Insight 1
# Most common accident hour
if "HOUR" in df.columns:
    most_common_hour = df["HOUR"].mode()[0]
    insight1 = f"The most common accident hour is {most_common_hour}."
else:
    insight1 = "HOUR column not found."

with open("insight1.txt", "w") as f:
    f.write(insight1)

# Insight 2
# Borough with most accidents
if "borough" in df.columns:
    top_borough = df["borough"].value_counts().idxmax()
    insight2 = f"The borough with the highest number of accidents is {top_borough}."
else:
    insight2 = "borough column not found."

with open("insight2.txt", "w") as f:
    f.write(insight2)

# Insight 3
# Most vehicle 1 category involved in accidents
if "vehicle_1_category" in df.columns:
    top_category = df["vehicle_1_category"].value_counts().idxmax()
    insight3 = f"The most common vehicle 1 category involved in accidents is {top_category}."
else:
    insight3 = "vehicle_1_category column not found."

with open("insight3.txt", "w") as f:
    f.write(insight3)

# Insight 4
# Average injuries per accident
if "persons_injured" in df.columns:
    avg_injuries = df["persons_injured"].mean()
    insight4 = f"The average number of injuries per accident is {avg_injuries:.2f}."
else: 
    insight4 = "persons_injured column not found."

with open("insight4.txt", "w") as f:
    f.write(insight4)

# Call visualization script
subprocess.run(["python", "visualize.py", input_path])