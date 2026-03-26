# CSCI461 Assignment 1: NYC Collisions Data Pipeline

## 👥Team Members
* Marwan Ayman Mohammed - ID: 231000704
* Mahmoud Hassan - ID: 231000496
* Mohamed Bassel - ID: 231001215
* Mazen Kamal - ID: 231002151

## Project Description
This project implements an automated Big Data processing pipeline using Docker. It ingests a raw dataset of NYC Motor Vehicle Collisions, preprocesses the data, generates text insights, visualizes the data, and performs K-Means clustering.

## 🐳Docker Commands Used
To reproduce this project, we used the following commands:

**1. Build the Docker Image:**
`docker build -t 1marwan1/nyc_motor_vehicle_collisions_sample .`

**2. Run the Container (Interactive Mode):**
`docker run -it -v $(pwd)/results:/app/pipeline/results --name analytics-container 1marwan1/nyc_motor_vehicle_collisions_sample bash`

*(Note: Once inside the container, the pipeline is triggered by running: `python ingest.py nyc_motor_vehicle_collisions_sample.csv`)*

## Execution Flow
1. **Data Ingestion (`ingest.py`):** Accepts the raw dataset path, loads it, saves it as `data_raw.csv`, and triggers the preprocessing script.
2. **Preprocessing (`preprocess.py`):** Cleans the data, performs feature transformation, and handles discretization. Saves the output to `data_preprocessed.csv`.
3. **Analytics (`analytics.py`):** Generates textual insights from the collisions data and saves them.
4. **Visualization (`visualize.py`):** Generates meaningful plots and saves them as `summary_plot.png`.
5. **Clustering (`cluster.py`):** Applies K-Means clustering on collision features and outputs sample counts.
6. **Summary (`summary.sh`):** Copies all generated files to the host machine's `results/` folder and stops the container.

## Sample Outputs
