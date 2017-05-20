#!/bin/bash

cd `dirname $BASH_SOURCE`/..

rm -f results/words/* 
rm -f results/meta/*

python src/predict_all.py -i tmp/Mnatobi_1924_N03-009.png

