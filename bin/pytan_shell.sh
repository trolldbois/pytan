#!/bin/sh

my_path=$0
my_script=`basename ${my_path}`
my_dirname=`dirname ${my_path}`
my_dir=`cd ${my_dirname} ; pwd`

. ${my_dir}/config.sh

for a in "${@}"; do pargs="${pargs}'${a}' "; done

if ! echo "${pargs}" | grep -- "'--help'\|'--version'" 2>&1 > /dev/null; then
    export PYTHONINSPECT="True"
fi

spew "Executing: \"${PYTHON_BINARY}\" ${PYTHON_OPTIONS} \"${WORKER_PATH}\" \"shell:${my_script}\" ${pargs}"
"${PYTHON_BINARY}" ${PYTHON_OPTIONS} "${WORKER_PATH}" "shell:${my_script}" "${@}"
EXITCODE=$?
spew "Exited with exit code: ${EXITCODE}"
exit ${EXITCODE}
