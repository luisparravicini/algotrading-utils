#!/bin/sh

dir=`dirname "$0"`
cd "$dir"

python -m updater.main $1 $2 $3
