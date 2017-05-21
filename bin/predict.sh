#!/bin/bash

cd `dirname $BASH_SOURCE`/..

rm -f results/words/* 
rm -f results/meta/*

python src/predict_all.py -i tests/Mnatobi-009-cropped.png

