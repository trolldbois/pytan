#!/bin/bash
script="${0}"
myscript=`basename "${script}"`
mydir=`dirname "${script}"`
mydir=`cd "${mydir}" ; pwd`
parentdir=`cd "${mydir}"/.. ; pwd`
basescript="${myscript%%.*}"

. "${mydir}"/API_INFO.sh

"${parentdir}"/${basescript}.py \
    -u "${username}" \
    -p "${password}" \
    --host "${host}" \
    --loglevel "${loglevel}" \
    --format "${ftype}" \
    --dirname "${fdir}" \
    --sensor 'Computer Name' \
    --sensor 'Installed Applications'
