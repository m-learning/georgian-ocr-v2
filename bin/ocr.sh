#!/bin/bash

cd `dirname $BASH_SOURCE`/..

rm -f results/words/* 
rm -f results/meta/*

python src/predict_all.py -i $1
python src/export.py $1 results/meta exported.svg exported-no-bg.svg
python src/export-fragments.py $1 results/meta results/words exported-fragments.svg

