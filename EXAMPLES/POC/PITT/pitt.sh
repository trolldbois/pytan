#!/bin/sh

my_path=$0
my_script=`basename ${my_path}`
my_dirname=`dirname ${my_path}`
my_dir=`cd ${my_dirname} ; pwd`

. ${my_dir}/config.sh

WORKER_PATH="${my_dir}/pitt.py"

spew "Executing: \"${PYTHON_BINARY}\" ${PYTHON_OPTIONS} \"${WORKER_PATH}\" ${PASSED_ARGS}"
"${PYTHON_BINARY}" -i ${PYTHON_OPTIONS} "${WORKER_PATH}" "${@}"
EXITCODE=$?
spew "Exited with exit code: ${EXITCODE}"
exit ${EXITCODE}
