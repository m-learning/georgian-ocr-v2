#!/bin/bash

cd `dirname $BASH_SOURCE`/..

rm -f results/words/* 
rm -f results/meta/*

python src/fragmenter.py tmp/Mnatobi-009-cropped.png

