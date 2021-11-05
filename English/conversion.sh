#!/bin/bash
sed '/2021/d;/^\s*$/d' $1 > mcc
#data=$(cat temp)
file="mcc"
echo "------"
j=0
shell_save="s"$1
clear_save="c"$1
md_save="m"$1
for i in $(cat $file)
do
    j=$((j+1))
    echo $j
    #data=$(wd $i)
	wd $i >> $shell_save
	#wd $data >> $shell_save
    #echo $data
done
rm mcc
cp $shell_save $clear_save
# 以下格式方清除颜色
sed -i 's/\[31m//' $clear_save
sed -i 's/\[31m//' $clear_save
sed -i 's/\[32m//' $clear_save
sed -i 's/\[33m//' $clear_save
sed -i 's/\[0m//' $clear_save
sed -i 's/\[36m//' $clear_save
sed -i 's/\[34m//' $clear_save
sed -i 's/\[36m//' $clear_save
sed -i 's/\[31m//' $clear_save
sed -i 's/\[0m//' $clear_save
sed -i 's///' $clear_save
sed -i 's///' $clear_save
sed -i 's///' $clear_save
sed -i 's///' $clear_save

sed -i G $clear_save  # 添加空行

cp $shell_save $md_save
# 以下方便md格式查看
sed -i 's/\[31m/<font color=Red>/' $md_save	# 将终端红色转换为md红色
sed -i 's/\[31m/<font color=Red>/' $md_save	
sed -i 's/\[31m/<font color=Red>/' $md_save	
sed -i 's/\[32m/<font color=Green>/' $md_save	# 将终端绿色转换为md绿色	
sed -i 's/\[33m/<font color=Yellow>/' $md_save	# 将终端黄色转换为md黄色
sed -i 's/\[34m/<font color=Blue>/' $md_save	# 将终端蓝色转换为md蓝色
sed -i 's/\[36m/<font color=Teal>/' $md_save	# 将终端蓝绿色转换为md蓝绿色
sed -i 's/\[36m/<font color=Teal>/' $md_save
sed -i 's/\[36m/<font color=Teal>/' $md_save

sed -i 's/\[0m/<\/font>/' $md_save	# 匹配<font>标志
sed -i 's/\[0m/<\/font>/' $md_save

sed -i 's///' $md_save
sed -i 's///' $md_save
sed -i 's///' $md_save
sed -i 's///' $md_save

sed -i G $md_save  # 添加空行
