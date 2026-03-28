import sys
import pandas as pd
import subprocess
from sklearn.cluster import KMeans

file_path = sys.argv[1]
df = pd.read_csv(file_path)

df.columns = df.columns.str.strip().str.lower()

cols = [
    'number_of_persons_injured',
    'number_of_persons_killed',
    'number_of_pedestrians_injured',
    'number_of_pedestrians_killed'
]

data = df[cols].fillna(0)

kmeans = KMeans(n_clusters=3, random_state=42)
df['cluster'] = kmeans.fit_predict(data)

counts = df['cluster'].value_counts().sort_index()

with open("clusters.txt", "w") as f:
    for cluster_id, count in counts.items():
        f.write(f"Cluster {cluster_id}: {count} samples\n")

print("Clusters saved")

# call next script
subprocess.run(["bash", "summary.sh", "clusters.txt"])
