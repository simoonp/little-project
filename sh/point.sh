#!/usr/bin/expect

set timeout 5

set name [lindex $argv 0]
set ip [lindex $argv 1]
set pw [lindex $argv 2]

#spawn ssh nxbot2@192.168.3.169
spawn ssh $name@$ip
expect "*password"

#send "666\r"
send "$pw\r"

expect "*login"

send "roslaunch smart_nav point.launch\r"

expect "move to"

send "1\r"
interact	
