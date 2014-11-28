#!/bin/bash
# this generates the /api/ dir under ../pytan/
script="${0}"
myscript=`basename "${script}"`
mydir=`dirname "${script}"`
mydir=`cd "${mydir}" ; pwd`
rootdir=`cd "${mydir}"/../ ; pwd`
pytandir=`cd "${rootdir}"/pytan ; pwd`
taniumpydir=`cd "${rootdir}"/../taniumpy ; pwd`

$taniumpydir/BUILD/generate_api.py -i $taniumpydir/BUILD/console.wsdl -o ${rootdir}/pytan -f
echo "Moving old api.* directories under ${rootdir}/pytan to $TMPDIR"
mv ${rootdir}/pytan/api.* $TMPDIR
