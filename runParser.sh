#!/bin/bash
counter=0
python3 ./parser.py
while [ $counter -le 39 ]
do
echo $counter
python3 ./parser.py ./items-$counter.json
((counter++))
done
echo All done