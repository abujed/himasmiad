#!/bin/bash

# This script takes a *.pcap as its input and spits out a csv ready to run against a classifier model trained by earlier work following 
# Markey's instructions in appendix A of his paper Using Decision Tree Analysis for Intrusion Detection: A How-To Guide
# This script is called by markey.pcapmod.agent.py

# BENT could be MALICIOUS, NORMAL, or SCANNING, but in this case is is missing value
# since we'll be running it against an already built model to classify the instances

NOW=$(date "+%Y%m%d%H%M")
BENT=""

# Convert PCAP to CSV
        # tcptrace does its magic and dumps the results to a tmp file
        tcptrace --csv -l ./output/$1 > ./output/$1.tmp
        # remove first 8 lines from the file
        sed -i -e '1,8d' ./output/$1.tmp
        # change the name of a column because I couldn’t find “session_duration” in the pcaps, I substituted some other duration column
        sed -i 's/idletime_max_a2b/session_duration/g' ./output/$1.tmp
        # remove the ,,, from this artifact line that somehow showed up (could probably do this all in one line - see next line)
        sed -i '/,,,,/d' ./output/$1.tmp
        # remove blank lines (could probably have matched the ,,,, and deleted all in one line, but this is helpful to know too :)
        sed -i '/^$/d' ./output/$1.tmp
        # csvtool yanks out only the columns we want
        csvtool col 4,5,8,9,22,23,84 ./output/$1.tmp >> ./output/$1.csv
        # sed -i '/^port_a/ s/$/,Class/' ./output/$1.csv
        # append ",NORMAL" or "MALICIOUS" (depending on variable above) to every line that does NOT have "port_a" in it
        # effectively populating the rows with whatever’s in the variable above (i.e. NORMAL) in the new column
        # sed -i "/^port_a/! s/$/,$BENT/" ./output/$1.csv
        # cleanup
        rm ./output/$1.tmp

# Convert CSV to ARFF
java -cp /usr/share/java/weka.jar weka.core.converters.CSVLoader ./output/$1.csv > ./output/$1.tmp.arff

# Convert the 8th column (of '?') from numeric to nominal so j48 will work
#java -cp /usr/share/java/weka.jar weka.filters.unsupervised.attribute.NumericToNominal -R 8 -i $1.tmp.arff -o $1.arff -c last

# append ",Class" to the end of the line that has "port_a" in it - effectively giving us a new column heading
java -cp /usr/share/java/weka.jar weka.filters.unsupervised.attribute.Add -T NOM -N Class -L NORMAL,MALICIOUS -C last -i ./output/$1.tmp.arff -o ./output/classifier.ready.$NOW.$1.arff


# cleanup
rm ./output/$1.csv
rm ./output/$1.tmp.arff
#rm ./output/$1.arff
rm ./output/$1
