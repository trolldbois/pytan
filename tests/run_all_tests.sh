#!/bin/bash -e
script="${0}"
myscript=`basename "${script}"`
mydir=`dirname "${script}"`
mydir=`cd "${mydir}" ; pwd`

cd ${mydir}
./run_api_tests.sh
./run_pytan_unittests.sh
./run_pytan_functests.sh
