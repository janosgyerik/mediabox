#!/bin/sh

cd $(dirname "$0")
. ./virtualenv.sh || exit 1

if test $# = 0; then
    python manage.py help
else
    python manage.py $*
fi
