#!/bin/bash

# this removes a bunch of columns making the arff suitable for apriori mining
# takes one argument which is the arff you wish to convert 

NOW=$(date "+%Y%m%d%H%M")

#java -mx1024m -cp /usr/share/java/weka.jar weka.filters.unsupervised.attribute.Remove -R 2-5,7-12,14-34,36-38,40-41,44,50-53,55-56,60-62,67-68,71-73,76,78-85,87,89-90,92-97,99,102,104-107,109,112-115,118-128,134-200  -i $1 -o ./output/$NOW.$1.tmp.arff

java -mx2048m -cp /usr/share/java/weka.jar weka.filters.unsupervised.attribute.Remove -V -R 1-10  -i ./output/$1.arff -o ./output/$NOW.$1.tmp.arff

java -mx2048m -cp /usr/share/java/weka.jar weka.filters.unsupervised.attribute.StringToNominal -R first-last  -i ./output/$NOW.$1.tmp.arff  -o ./output/apriori.ready.$NOW.$1.arff

#cleanup
rm ./output/$NOW.$1.tmp.arff
rm ./output/$1.pdml
rm ./output/$1.arff
rm ./output/$1
