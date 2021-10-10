#!/bin/bash
counter=0
python3 ./skeleton_parser_duncan.py
while [ $counter -le 39 ]
do
echo $counter
python3 ./skeleton_parser_duncan.py ./items-$counter.json
((counter++))
done
echo All done