#!/bin/sh -e

cd $(dirname "$0")/..

if git ls-files -m | grep -q .; then
    echo Fixing dos line endings is not safe with pending changes.
    echo Commit pending changes first and rerun this script.
    exit 1
fi

./scripts/find-dos.sh | while read path; do
    echo fixing $path ...
    git show HEAD:$path | tr -d '\r' > $path
done
