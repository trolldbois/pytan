#!/bin/sh

# Configuration file for PyTan .sh scripts

if [ -z "${PYTHON_BINARY}" ]; then
    PYTHON_BINARY="python"
    #PYTHON_BINARY="python3"
fi

spew(){ test -n "${SHELL_DEBUG}" && echo "$@";}

if [ -z "${my_dir}" ]; then
    echo "Need 'my_dir' defined to know where config.sh lives"
    exit 99
fi

parent_dirname=`dirname ${my_dir}`
parent_dir=`cd ${parent_dirname} ; pwd`
pytan_pkg_dir=`cd ${parent_dir}/pytan ; pwd`
pytan_ext_dir=`cd ${pytan_pkg_dir}/ext ; pwd`

if [ -n "${PYTAN_PATH}" ]; then
    PYTAN_PATH=`cd ${PYTAN_PATH} ; pwd`
    PYTHONPATH="${PYTAN_PATH}:${PYTHONPATH}"
fi

for a in "${@}"; do PASSED_ARGS="${PASSED_ARGS}'${a}' "; done

PYTHONPATH="${parent_dir}:${PYTHONPATH}"
PYTHONDONTWRITEBYTECODE="True"
PYTHON_VERSION=`"${PYTHON_BINARY}" --version 2>&1`
spew "Using Python binary '${PYTHON_BINARY}' version: ${PYTHON_VERSION}"

export PYTHONPATH PYTHONDONTWRITEBYTECODE PYTHON_VERSION
