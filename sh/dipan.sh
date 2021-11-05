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

#send "echo ok \r"
send "roslaunch rikibot bringup_old.launch\r"
interact	
