#!/bin/sh

split -n 3 -d -a 1 data.txt data_

mv data_2 data_3
mv data_1 data_2
mv data_0 data_1

for i in 1 2 3
do 
    mkdir mapa_$i
    mv data_$i mapa_$i
done

