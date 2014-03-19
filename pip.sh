#!/bin/bash

cd $(dirname "$0")
. ./virtualenv.sh || exit 1

pip $*
