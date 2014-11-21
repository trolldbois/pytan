#!/bin/bash
# this generates all the windows batch scripts that are in winbin/
script="${0}"
myscript=`basename "${script}"`
mydir=`dirname "${script}"`
mydir=`cd "${mydir}" ; pwd`
parentdir=`cd "${mydir}"/.. ; pwd`
basescript="${myscript%%.*}"

bindir=`cd "${parentdir}/bin"; pwd`
winbindir="${parentdir}/winbin"

for i in "${bindir}"/*.py ; do
    pyfile=`basename "${i}"`
    basefile="${pyfile%%.*}"
    if head -1 "$i" | grep -q -- '-i' &> /dev/null ; then
        TEMPLATE_BAT="${mydir}/IA_TEMPLATE.bat"
    else
        TEMPLATE_BAT="${mydir}/TEMPLATE.bat"
    fi
    echo cp "${TEMPLATE_BAT}" "${winbindir}/${basefile}".bat
    cp "${TEMPLATE_BAT}" "${winbindir}/${basefile}".bat
done

for i in "${winbindir}"/*.bat ; do
    batfile=`basename "${i}"`
    test "${batfile}" == "CONFIG.bat" && continue
    basefile="${batfile%%.*}"
    test -f "${bindir}/${basefile}".py || echo "Remove ${i}?"
done
