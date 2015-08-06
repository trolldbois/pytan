#!/bin/bash

# This is a simple bash script that can be used to fetch the info page in JSON format using curl

server="172.16.31.128"
port="443"
username="Tanium User"
password='T@n!um'
output_file='server_info.json'

touch $output_file
curl -u "${username}:${password}" -k -X POST "https://${server}:${port}/info.json" -o $output_file
echo "Saved info.json to $output_file"
