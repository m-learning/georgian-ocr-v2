#!/bin/bash

cd `dirname $BASH_SOURCE`/..

python src/export.py tmp/monochrome.png results/meta tmp/exported.svg

