#!/bin/bash

cd `dirname $BASH_SOURCE`/..

python src/export.py Mnatobi_1924_N03-009.png results/meta tmp/exported.svg
python src/export-fragments.py Mnatobi_1924_N03-009.png results/meta results/words tmp/exported-fragments.svg

