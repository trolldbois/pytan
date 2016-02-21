#!/bin/sh

my_path=$0
my_script=`basename ${my_path}`
my_dirname=`dirname ${my_path}`
my_dir=`cd ${my_dirname} ; pwd`

. ${my_dir}/config.sh

export PYTHONINSPECT="True"
WORKER_PATH="${my_dir}/worker.py"

spew "Executing: \"${PYTHON_BINARY}\" ${PYTHON_OPTIONS} \"${WORKER_PATH}\" \"shell:${my_script}\" ${PASSED_ARGS}"
"${PYTHON_BINARY}" ${PYTHON_OPTIONS} "${WORKER_PATH}" "shell:${my_script}" "${@}"
EXITCODE=$?
spew "Exited with exit code: ${EXITCODE}"
exit ${EXITCODE}
