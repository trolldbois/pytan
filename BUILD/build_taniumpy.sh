#!/bin/bash
# this generates the taniumpy/ dir under ../pytan/
# this uses the taniumpy github repo, and should not be done unless you are absolutely sure
# you know you want to!!!!!
script="${0}"
myscript=`basename "${script}"`
mydir=`dirname "${script}"`
mydir=`cd "${mydir}" ; pwd`
rootdir=`cd "${mydir}"/../ ; pwd`
pytandir=`cd "${rootdir}"/pytan ; pwd`
taniumpydir=`cd "${rootdir}"/../taniumpy ; pwd`

$taniumpydir/BUILD/generate_api.py -i $taniumpydir/BUILD/console.wsdl -o ${rootdir}/lib -v
rm -rf ${rootdir}/lib/taniumpy
mv ${rootdir}/lib/api ${rootdir}/lib/taniumpy
echo "Moved ${rootdir}/lib/api to ${rootdir}/lib/taniumpy"
