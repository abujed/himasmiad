#!/bin/bash

# this script is called by dm.agent.classify.j48.01.py
# it ingests an arff and the spits out a output file
# -l is the model we're testing against (could be variablized)
# -p 8 is the attribute we're trying to predict.  (could also be variablized) 
# -T $1 is the path/to/name.arff of the test arff

NOW=$(date "+%Y%m%d%H%M")

java -mx1024m -cp /usr/share/java/weka.jar weka.classifiers.trees.J48 -l ./models/j48.markey.traffic.analysis.model2.model -p 8 -T ../../preprocessing/classify/output/$1 > ./output/$1.j48.02.$NOW.out

