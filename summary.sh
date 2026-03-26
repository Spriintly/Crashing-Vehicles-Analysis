#!/bin/bash

CONTAINER_NAME=analytics
DEST_DIR=customer-analytics/results

echo "Creating results directory"
mkdir -p $DEST_DIR

echo "Copying results from container"

docker cp $CONTAINER_NAME:/app/pipeline/data_raw.csv $DEST_DIR/
docker cp $CONTAINER_NAME:/app/pipeline/data_preprocessed.csv $DEST_DIR/

docker cp $CONTAINER_NAME:/app/pipeline/insight1.txt $DEST_DIR/
docker cp $CONTAINER_NAME:/app/pipeline/insight2.txt $DEST_DIR/
docker cp $CONTAINER_NAME:/app/pipeline/insight3.txt $DEST_DIR/

docker cp $CONTAINER_NAME:/app/pipeline/summary_plot.png $DEST_DIR/
docker cp $CONTAINER_NAME:/app/pipeline/clusters.txt $DEST_DIR/

echo "Stopping container"
docker stop $CONTAINER_NAME

echo "Removing container"
docker rm $CONTAINER_NAME

echo "Done. Results saved in $DEST_DIR"