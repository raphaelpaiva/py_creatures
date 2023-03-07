#!/bin/sh

TIMESTAMP=`date +%s`
FILENAME_TEMPLATE="benchmark_$TIMESTAMP"
PROFILE_FILENAME="$FILENAME_TEMPLATE.prof"
CALLTREE_FILENAME="$FILENAME_TEMPLATE.calltree"

python -m cProfile -o $PROFILE_FILENAME main.py scenarios/movearound.yaml -b
pyprof2calltree -i $PROFILE_FILENAME -o $CALLTREE_FILENAME