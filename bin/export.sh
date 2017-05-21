#!/bin/bash

cd `dirname $BASH_SOURCE`/..

python src/export.py tests/Mnatobi-009-cropped.png results/meta exported.svg
python src/export-fragments.py tests/Mnatobi-009-cropped.png results/meta results/words exported-fragments.svg

