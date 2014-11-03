#!/bin/bash
script=$0
myscript=`basename $script`
mydir=`dirname $script`
mydir=`cd $mydir ; pwd`
parentdir=`cd $mydir/.. ; pwd`
basescript="${myscript%%.*}"

. $mydir/API_INFO.sh

$parentdir/${basescript}.py -u "$username" -p "$password" --host "$host" --loglevel $loglevel --format $ftype --dirname $fdir --objtype "sensor" --query "Installed Applications" --query "Computer Name"

$parentdir/${basescript}.py -u "$username" -p "$password" --host "$host" --loglevel $loglevel --format $ftype --dirname $fdir --objtype "package" --query "all"
