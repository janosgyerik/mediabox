#!/bin/bash -e

cd $(dirname "$0")/..
. scripts/include.sh

locale_params=()
for lang in ${langs[@]}; do
    locale_params+=(-l $lang)
done

makemessages() {
    appdir=$1; shift
    msg makemessages for $appdir ...
    mkdir -p $appdir/locale
    (cd $appdir && python ../manage.py makemessages ${locale_params[@]} $*)
}

for app in ${apps[@]}; do
    makemessages $app $*
done
