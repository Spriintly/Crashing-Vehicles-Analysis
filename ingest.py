import sys
import subprocess
import pandas as pd

pd.read_csv(sys.argv[1]).to_csv("data_raw.csv", index=False)
subprocess.run(["python", "preprocess.py", "data_raw.csv"])