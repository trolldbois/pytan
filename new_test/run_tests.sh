#!/bin/sh

my_path=$0
my_script=`basename ${my_path}`
my_dirname=`dirname ${my_path}`
my_dir=`cd ${my_dirname} ; pwd`
bin_dir=`cd ${my_dir}/../bin ; pwd`

export SHELL_DEBUG="True"

. ${bin_dir}/config.sh

export PYTHONPATH="${PYTHONPATH}:${pytan_ext_dir}"

PYTEST_BINARY="${pytan_ext_dir}/pytest.py"
PYTEST_OPTIONS=-rsefwx

cd "${my_dir}"

spew "Executing: \"${PYTHON_BINARY}\" ${PYTHON_OPTIONS} \"${PYTEST_BINARY}\" ${PYTEST_OPTIONS} ${PASSED_ARGS}"
"${PYTHON_BINARY}" ${PYTHON_OPTIONS} "${PYTEST_BINARY}" ${PYTEST_OPTIONS} "${@}"
EXITCODE=$?
spew "Exited with exit code: ${EXITCODE}"
exit ${EXITCODE}
