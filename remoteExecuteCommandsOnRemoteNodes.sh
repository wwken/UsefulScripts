#!/bin/bash

# 2015 Ken Wu
# This script is looping through the /etc/hosts file to execute the commands on all the matched slave nodes

slaveNodePrefix="ken-cluster-node"
sshKey="/home/ubuntu/.ssh/sshkey.rsa"
commands="cd scripts; ./restartMesosSlave.sh; "		#this is the command(s) you want to execute remotely"

for pp in `cat /etc/hosts`; do
        if [[ ${pp} = "$slaveNodePrefix"*  ]]; then
                echo "On ${pp} ..., executing command: $commands";
                ssh -i $sshKey ${pp} $commands
                #echo "$c"
        fi
done
