#!/bin/bash
# this generates the /api/ dir under ../pytan/
script="${0}"
myscript=`basename "${script}"`
mydir=`dirname "${script}"`
mydir=`cd "${mydir}" ; pwd`
rootdir=`cd "${mydir}"/../ ; pwd`


cd ${mydir}/build_api
./generate_api.py -i console.wsdl -o ${rootdir}/pytan -f
echo "Moving old api.* directories under ${rootdir}/pytan to $TMPDIR"
mv ${rootdir}/pytan/api.* $TMPDIR
