#!/bin/bash

for FILE in frame-*; do
       echo "$FILE"
       sbatch ${FILE}
       sleep 2s
done
