#!/bin/bash

cd `dirname $BASH_SOURCE`/..

rm -f results/letters/* 
rm -f results/meta/*
rm -f results/words/*

python src/fragmenter.py tests/Mnatobi-009-cropped.png

