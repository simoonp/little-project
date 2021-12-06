#!/bin/bash

echo "输入名称 ip 密码"
name=$1
ip=$2
pw=$3
echo "开启底盘"
gnome-terminal -t 'dp' -- ~/sh/dipan.sh $1 $2 $3
echo "开启导航"
sleep 10s
gnome-terminal -t 'nav' -- ~/sh/nav.sh $1 $2 $3

echo "打开rviz"
sleep 5s
gnome-terminal -t 'rviz' -- rviz

#y="y"
echo "是否已经手动定位完成？(y o n)"
while read flag;do
#read flag
	if [ "$flag" = "y" ];then
		echo "开始定点导航"
		gnome-terminal -t 'nav' -- ~/sh/point.sh $1 $2 $3
		break
	elif [ "$flag" == "0" ]
	then
		break
	fi
	echo "等待完成(输入0直接退出)"
done
