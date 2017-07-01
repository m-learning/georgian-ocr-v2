#!/bin/bash

cd `dirname $BASH_SOURCE`/..

rm -f results/debug/* 
rm -f results/meta/* 
rm -f results/zones/*

python src/fragment_zones.py tmp/Mnatobi_1924_N03-009.png
#python src/fragment_zones.py tmp/Iveria_1905_N30.png
#python src/fragment_zones.py tmp/Ciskari_1852_N12-004.png

