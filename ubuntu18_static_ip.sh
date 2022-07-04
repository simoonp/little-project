#! /bin/bash   

cd /etc/netplan
pwd
num=0;
for filename in $(ls .)
do
	let num=1+$num
done
# echo $i
# echo $num
if (($num == 1))
then	
	echo "文件获取成功"
	# echo $1	
	echo "即将修改配置文件：$filename"
	cp $filename $filename.old
	# echo "安装所需的软件 net-tools git"
	# sudo apt install net-tools
	# sudo apt install git
	echo "输入需要配置的网卡："
	read net_name
	
	echo "输入静态IP:"
	read static_ip
	
	echo "是否开启dhcp？(yes/no，默认 no)"
	read t_dhcp
	if [ -z "${t_dhcp}"];then
		t_dhcp=no
	fi
	echo $t_dhcp

	echo "输入子网掩码对应的十进制格式(默认 24)"

	read child
	if [ -z "${child}"];then        
		child=24
	fi
	echo $child

	echo "输入IP的网关"
	read t_gate

	echo "设置DNS(默认为网关)"
	read t_dns
	if [ -z "${t_dns}" ];then
		t_dns=$t_gate
	fi

	echo "检查输入的信息是否正确(y/n，n退出配置， 默认y)"
	echo "网卡：$net_name"
	echo "IP: $static_ip"
	echo "dhcp? $t_dhcp"
	echo "子网掩码：$child"
	echo "网关： $t_gate"
	echo "DNS: $t_dns"
	read ok
	if [ -z ""${ok} ];then
		ok=y
	fi
	
	if (($ok == y))
	then
		echo "开始配置"
		echo -e "  ethernets:" >> $filename
		echo -e "    $net_name:" >> $filename
		echo -e "      dhcp4: $t_dhcp" >> $filename
		echo -e "      addresses: [$static_ip/$child]" >> $filename
		echo -e "      gateway4: $t_gate" >> $filename
		echo -e "      nameservers:" >> $filename
		echo -e "        addresses: [$t_dns]" >> $filename
	else
		exit
	fi
	sudo netplan apply 
	echo "请重启计算机"

else
	echo "存在多个文件，请手动配置"
fi

