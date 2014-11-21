#!/bin/bash
script="${0}"
myscript=`basename "${script}"`
mydir=`dirname "${script}"`
mydir=`cd "${mydir}" ; pwd`

python -ttB -m unittest  discover -v ${mydir}/api
