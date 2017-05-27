#!/bin/bash

cd `dirname $BASH_SOURCE`/..

rm -f results/words/* 
rm -f results/meta/*
rm -f results/letters/*

python src/predict_all.py -i $1
python src/export.py $1 results/meta exported.svg exported-no-bg.svg
python src/export_fragments.py $1 results/meta results/words exported-fragments.svg
python src/export_words.py

