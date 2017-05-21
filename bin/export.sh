#!/bin/bash

cd `dirname $BASH_SOURCE`/..

python src/export.py tests/Mnatobi-009-cropped.png results/meta exported.svg exported-no-bg.svg
python src/export-fragments.py tests/Mnatobi-009-cropped.png results/meta results/letters exported-fragments.svg

