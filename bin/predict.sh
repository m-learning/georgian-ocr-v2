#!/bin/bash

cd `dirname $BASH_SOURCE`/..

rm -f results/letters/* 
rm -f results/meta/*
rm -f results/words/*

python src/predict_all.py -i tests/Mnatobi-009-cropped.png



