#!/bin/bash

cd $1

echo "Converting $1 to json"
for f in *.abc
do ../abcparser/abc2midi "$f" > "${f%.abc}.json"
done

echo "Done!"

grep Warning *.json > warnings.txt
grep Error *.json > errors.txt
