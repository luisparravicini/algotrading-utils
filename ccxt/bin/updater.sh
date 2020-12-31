#!/bin/sh

# this file is intended to run inside the Docker container


dir=`dirname "$0"`
cd "$dir"

python -m updater.main $1 $2 $3
