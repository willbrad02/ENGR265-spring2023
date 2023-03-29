#!/bin/bash

rdsamp -r $1/$2 -c -v -p > $1_$2.csv
rdann -r $1/$2 -a atr >$1_$2_annotations.txt
