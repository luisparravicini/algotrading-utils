#!/bin/sh

dir=`dirname "$0"`
cd "$dir"/..

python -m updater.main update $1 $2 $3
