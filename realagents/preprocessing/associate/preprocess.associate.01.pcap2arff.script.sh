#!/bin/bash

# convert pcap to pdml
tshark -T pdml -r ./output/$1 > ./output/$1.pdml

# convert pdml to arff (this could take a while)
pdml2arff.py ./output/$1.pdml
