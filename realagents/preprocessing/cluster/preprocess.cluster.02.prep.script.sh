#!/bin/bash

# this removes a bunch of columns making the arff suitable for apriori mining
# takes one argument which is the arff you wish to convert 

NOW=$(date "+%Y%m%d%H%M")

# convert pcap to pdml
tshark -T pdml -r ./output/$1 > ./output/$1.pdml

# convert pdml to arff (this could take a while)
pdml2arff.py ./output/$1.pdml

# remove attributes except ip.src and ip.dst
# works with example-5.com
java -mx1024m -cp /usr/share/java/weka.jar weka.filters.unsupervised.attribute.Remove -V -R 36,40 -i ./output/$1.arff -o ./output/$1.2attrib.arff

# call the pythonese stripq script
./preprocess.cluster.03.stripq.py ./output/$1.2attrib.arff

# convert strings to nominal
java -mx1024m -cp /usr/share/java/weka.jar weka.filters.unsupervised.attribute.StringToNominal -R first-last  -i ./output/$1.2attrib.noq.arff  -o ./output/cluster.ready.$1.$NOW.arff


#cleanup
rm ./output/$1.2attrib.noq.arff
rm ./output/$1.2attrib.arff
rm ./output/$1.pdml
rm ./output/$1.arff
rm ./output/$1

