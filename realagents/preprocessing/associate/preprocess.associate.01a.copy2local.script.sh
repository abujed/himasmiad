#!/bin/bash

# $1 is the filename provided by an agent - should be oldest file in box directory

DROPDIR=/home/miner/himasmiad/fakeagents/dropoff/box/

# copy file to local dir
cp $DROPDIR/$1 ./output/
