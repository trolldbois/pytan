#!/bin/bash
script="${0}"
myscript=`basename "${script}"`
mydir=`dirname "${script}"`
mydir=`cd "${mydir}" ; pwd`

${mydir}/pytan/test_pytan_handler.py
