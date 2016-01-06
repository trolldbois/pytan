#!/bin/sh

my_path=$0
my_script=`basename ${my_path}`
my_dirname=`dirname ${my_path}`
my_dir=`cd ${my_dirname} ; pwd`

. ${my_dir}/config.sh

export PYTHONINSPECT="True"

for a in "${@}"; do pargs="${pargs}'${a}' "; done

spew "Executing: \"${PYTHON_BINARY}\" \"${WORKER_PATH}\" \"shell:${my_script}\" ${pargs}"
"${PYTHON_BINARY}" "${WORKER_PATH}" "shell:${my_script}" "${@}"
EXITCODE=$?
spew "Exited with exit code: ${EXITCODE}"
exit ${EXITCODE}
