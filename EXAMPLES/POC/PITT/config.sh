#!/bin/sh

# Configuration file for PyTan .sh scripts

# path to Pytan - change me accordingly!
PYTAN_PATH=/github/pytan

if [ -z "${PYTHON_BINARY}" ]; then
    PYTHON_BINARY="python"
    #PYTHON_BINARY="python3"
fi

spew(){ test -n "${SHELL_DEBUG}" && echo "$@";}

if [ -n "${PYTAN_PATH}" ]; then
    PYTAN_PATH=`cd ${PYTAN_PATH}/lib ; pwd`
    PYTHONPATH="${PYTAN_PATH}:${PYTHONPATH}"
fi

for a in "${@}"; do PASSED_ARGS="${PASSED_ARGS}'${a}' "; done

PYTHONPATH="${my_dir}:${PYTHONPATH}"
PYTHONDONTWRITEBYTECODE="True"
PYTHON_VERSION=`"${PYTHON_BINARY}" --version 2>&1`
spew "Using Python binary '${PYTHON_BINARY}' version: ${PYTHON_VERSION}"

export PYTHONPATH PYTHONDONTWRITEBYTECODE PYTHON_VERSION
