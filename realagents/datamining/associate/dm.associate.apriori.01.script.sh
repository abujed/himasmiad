#!/bin/bash

# this script generates output to a file using Apriori associator
# $1 is the name of the <input.arff> provided by the preprocessing prass01.py

#NOW=$(date "+%Y%m%d%H%M")

java -mx2048m -cp /usr/share/java/weka.jar weka.associations.Apriori -N 10 -T 0 -C 0.9 -D 0.05 -U 1.0 -M 0.1 -S -1.0 -c -1 -t ../../preprocessing/associate/output/$1 > ./output/dm.associate.apriori.$1.output
