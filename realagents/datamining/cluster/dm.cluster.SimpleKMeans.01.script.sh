#!/bin/bash

# this script generates output to a file using SimpleKMeans clusterer
# $1 is the <training.arff>

NOW=$(date "+%Y%m%d%H%M")

java -mx1024m -cp /usr/share/java/weka.jar weka.clusterers.SimpleKMeans -N 2 -A "weka.core.EuclideanDistance -R first-last" -I 500 -S 10 -t ../../preprocessing/cluster/output/$1 -d ./output/dm.cluster.SimpleKMeans.$1.$NOW.model > ./output/dm.cluster.SimpleKMeans.$1.$NOW.out
