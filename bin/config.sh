#!/bin/sh

# Configuration file for PyTan .sh scripts

if [ -z "${PYTHON_BINARY}" ]; then
    PYTHON_BINARY="python"
    #PYTHON_BINARY="python3"
fi

spew(){ test -n "${SHELL_DEBUG}" && echo "$@";}

my_path=$0
my_script=`basename ${my_path}`
my_dirname=`dirname ${my_path}`
my_dir=`cd ${my_dirname} ; pwd`
parent_dir=`cd ${my_dir}/.. ; pwd`
pytan_pkg_dir=`cd ${parent_dir}/pytan ; pwd`
pytan_ext_dir=`cd ${pytan_pkg_dir}/ext ; pwd`

if [ -n "${PYTAN_PATH}" ]; then
    PYTAN_PATH=`cd ${PYTAN_PATH} ; pwd`
    PYTHONPATH="${PYTAN_PATH}:${PYTHONPATH}"
fi

for a in "${@}"; do PASSED_ARGS="${PASSED_ARGS}'${a}' "; done

if echo "${PASSED_ARGS}" | grep -- "'--help'\|'--version'" 2>&1 > /dev/null; then
    PYTHONINSPECT=""
fi

PYTHONPATH="${parent_dir}:${PYTHONPATH}"
PYTHONDONTWRITEBYTECODE="True"
PYTHON_VERSION=`"${PYTHON_BINARY}" --version 2>&1`
spew "Using Python binary '${PYTHON_BINARY}' version: ${PYTHON_VERSION}"

WORKER_PATH="${my_dir}/worker.py"

export PYTHONPATH PYTHONDONTWRITEBYTECODE PYTHON_VERSION
