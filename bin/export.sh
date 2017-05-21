#!/bin/bash

cd `dirname $BASH_SOURCE`/..

python src/export.py Mnatobi-009-cropped.png results/meta tmp/exported.svg
python src/export-fragments.py Mnatobi-009-cropped.png results/meta results/words tmp/exported-fragments.svg

