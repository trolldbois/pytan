#!/bin/bash

# this is a bash script that will use curl to query the server over and over again for the sensor
# list. It can be used to "load test" a tanium server from a certain perspective, but it has a
# failing in that the connections are not re-used (so a new connection is opened for every attempt)

server="172.16.31.128"
port="443"
username="Tanium User"
password='T@n!um'
object_list='sensor'
output_file="test1234.out"

xml=$(cat << _EOF_
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<SOAP-ENV:Body><typens:tanium_soap_request xmlns:typens="urn:TaniumSOAP">
<auth><username>${username}</username><password>${password}</password></auth>
<command>GetObject</command><object_list><${object_list}/></object_list>
</typens:tanium_soap_request></SOAP-ENV:Body></SOAP-ENV:Envelope>
_EOF_
)

loop_count = 1
while true; do
  touch $output_file
  curl -v --connect-timeout 60 --keepalive-time 60 --ssl -k -X POST -d "${xml}" "https://${server}:${port}/soap" -o $output_file
  v=$?
  line_count=`cat $output_file| wc -l`
  echo exit code $v, lines returned: $line_count, loop count: $loop_count
  if test "$v" != "0" ; then
    echo "error encountered, output received: "
    cat $output_file
    break
  fi
  if test $line_count -lt 20 ; then
    echo "less than 20 lines received, output received: "
    cat $output_file
    break
  fi
  head $output_file
  rm -f $output_file
  let loop_count+=1
done
