#!/bin/bash

command="python /root/HomeAidPi/HomeAidPi.py & "

for var in "$@"
do
  command+=$var
  command+=" "
done

python /root/HomeAidPi/WebRemote.py &
$command

