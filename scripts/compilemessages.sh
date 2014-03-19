#!/bin/bash -e

cd $(dirname "$0")/..
. scripts/include.sh

compilemessages() {
    appdir=$1
    msg compilemessages for $appdir ...
    (cd $appdir && python ../manage.py compilemessages >/dev/null)
}

for app in ${apps[@]}; do
    compilemessages $app
done
