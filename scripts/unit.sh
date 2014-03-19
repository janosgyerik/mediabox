#!/bin/bash -e

cd $(dirname "$0")/..
. scripts/include.sh

./manage.sh test ${apps[@]}
