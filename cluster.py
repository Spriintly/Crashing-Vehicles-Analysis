import sys
import pandas as pd
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

output_path = "clustered_data.csv"
df.to_csv(output_path, index=False)

print("Clustering done")

# call next script
subprocess.run(["python", "summary.sh", output_path])