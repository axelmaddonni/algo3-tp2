#!/bin/bash

for ((i=1;i<=$3;i++)); do
  echo -n $i " " && java -jar $1 -exec $2 -test $i || break
done
