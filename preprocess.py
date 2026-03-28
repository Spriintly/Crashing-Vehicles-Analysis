import sys
import subprocess
import pandas as pd

# Read input file

input_path = sys.argv[1]

df = pd.read_csv(input_path)

# understand the data
df.info()

# Convert datetime
df["CRASH_DATETIME"] = pd.to_datetime(
    df["crash_date"].astype(str) + " " + df["crash_time"].astype(str),
    errors="coerce"
)

# Extract time features
df["HOUR"] = df["CRASH_DATETIME"].dt.hour
df["DAY"] = df["CRASH_DATETIME"].dt.day_name()
df["MONTH"] = df["CRASH_DATETIME"].dt.month

# Drop irrelevant columns
df.drop(columns=[
    'zip_code','latitude','longitude','crash_date','crash_time','location',
    'cross_street_name','off_street_name',
    'contributing_factor_vehicle_3','contributing_factor_vehicle_4','contributing_factor_vehicle_5',
    'vehicle_type_code_3','vehicle_type_code_4','vehicle_type_code_5',
    'collision_id'
], inplace=True, errors='ignore')

# Rename columns for better readability
df.rename(columns={
    'BOROUGH': 'borough',
    'ON STREET NAME': 'on_street',
    'NUMBER OF PERSONS INJURED': 'persons_injured',
    'NUMBER OF PERSONS KILLED': 'persons_killed',
    'NUMBER OF PEDESTRIANS INJURED': 'pedestrians_injured',
    'NUMBER OF PEDESTRIANS KILLED': 'pedestrians_killed',
    'NUMBER OF CYCLIST INJURED': 'cyclists_injured',
    'NUMBER OF CYCLIST KILLED': 'cyclists_killed',
    'NUMBER OF MOTORIST INJURED': 'motorists_injured',
    'NUMBER OF MOTORIST KILLED': 'motorists_killed',
    'VEHICLE TYPE CODE 1': 'vehicle_type_1',
    'VEHICLE TYPE CODE 2': 'vehicle_type_2',
    'CONTRIBUTING FACTOR VEHICLE 1': 'contributing_factor_1',
    'CONTRIBUTING FACTOR VEHICLE 2': 'contributing_factor_2',
    'CRASH_DATETIME': 'crash_datetime',
}, inplace=True)

# check the structure of the data again
df.info()

# check the data types and unique values of each column
dtypes = df.dtypes
uniqueValues = df.nunique()
pd.DataFrame({'Data Types': dtypes, 'Unique Values': uniqueValues}).T

# Convert data types
numeric_cols = [
    'persons_injured',
    'persons_killed',
    'pedestrians_injured',
    'pedestrians_killed',
    'cyclists_injured',
    'cyclists_killed',
    'motorists_injured',
    'motorists_killed'
]

categorical_cols = ['borough', 'DAY']
for col in categorical_cols:
    if col in df.columns:
        df[col] = df[col].astype('category')

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

string_cols = [
    'on_street',
    'contributing_factor_1',
    'contributing_factor_2',
    'vehicle_type_1',
    'vehicle_type_2'
]

for col in string_cols:
    if col in df.columns:
        df[col] = df[col].astype('string')

# check for null values
nulls = df.isna().sum()
ratio = (nulls / len(df)) * 100
pd.DataFrame({'Null Values': nulls, 'Ratio (%)': ratio}).T

# Handle nulls
df['borough'] = df['borough'].cat.add_categories('Unknown').fillna('Unknown')
df['on_street_name'] = df['on_street_name'].fillna('Unknown')

# vehicle_type_1 has many unique values, so we will fill nulls with the most common value (mode) if it exists
if 'vehicle_type_1' in df.columns and not df['vehicle_type_1'].mode().empty:
    df['vehicle_type_1'] = df['vehicle_type_1'].fillna(df['vehicle_type_1'].mode()[0])

# contributing_factor_1 has many unique values, so we will fill nulls with the most common value (mode) if it exists
if 'contributing_factor_1' in df.columns and not df['contributing_factor_1'].mode().empty:
    df['contributing_factor_1'] = df['contributing_factor_1'].fillna(df['contributing_factor_1'].mode()[0])

df['vehicle_type_code2'] = df['vehicle_type_code2'].fillna("Unknown")
df['contributing_factor_vehicle_2'] = df['contributing_factor_vehicle_2'].fillna("Unspecified")

# Remove duplicates
df.drop_duplicates(inplace=True)

# Outliers check
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns

for col in numeric_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]

    print(f"{col}: {len(outliers)} outliers")

# Encoding 
def categorize_contributing_factor(reason):
    if reason in ['Driver Inattention/Distraction', 'Aggressive Driving/Road Rage', 'Alcohol Involvement', 'Failure to Yield Right-of-Way', 'Unsafe Speed', 'Driver Inexperience', 'Fell Asleep', 'Texting']:
        return 'Driver Behavior'
    elif reason in ['Steering Failure', 'Brakes Defective', 'Oversized Vehicle', 'Other Vehicular']:
        return 'Vehicle Issue'
    elif reason in ['Pavement Slippery', 'Obstruction/Debris', 'Traffic Control Disregarded', 'View Obstructed/Limited']:
        return 'Environmental Factor'
    else:
        return 'Unspecified'

df['vehicle_1_category'] = df['contributing_factor_vehicle_1'].apply(categorize_contributing_factor)
df['vehicle_2_category'] = df['contributing_factor_vehicle_2'].apply(categorize_contributing_factor)

df['main_category'] = df['vehicle_1_category'].combine_first(df['vehicle_2_category'])

df_encoded = pd.get_dummies(df, columns=['main_category'])

# Drop original contributing factor columns
df_encoded.drop(['contributing_factor_vehicle_1', 'contributing_factor_vehicle_2'], axis=1, inplace=True)

# Save preprocessed data
output_path = "data_preprocessed.csv"
df_encoded.to_csv(output_path, index=False)

print("Preprocessing done. File saved as:", output_path)

# Call next script
subprocess.run(["python", "analytics.py", output_path])