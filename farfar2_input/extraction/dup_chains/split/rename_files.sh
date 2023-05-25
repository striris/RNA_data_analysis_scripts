# !/bin/bash

suffix=$1
destination_suffix=$2

for i in $(ls *.${suffix});do
	mv $i $(echo $i | sed s/${suffix}/${destination_suffix}/)
done
