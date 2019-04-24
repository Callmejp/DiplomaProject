#! /bin/bash

cd ../ERAN/tf-verify
/usr/python/bin/python3.6 __main__.py $1 0.12 ../data/mnist_test.csv
/usr/python/bin/python3.6 __main__.py $2 0.12 ../data/mnist_test.csv
cd 
cd mystite/

