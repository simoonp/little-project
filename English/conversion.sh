#!/bin/bash

if [ -n "$1" ]
then
    echo "转换的文件是$1"
else
    echo "没有输入文件"
    exit
fi

sed '/2021/d;/^\s*$/d' $1 > mcc
#data=$(cat temp)
file="mcc"
echo "------"
j=0
shell_save="s"$1
clear_save="c"$1
md_save="m"$1
eudic_save="e"$1
eudic_save=${eudic_save/md/txt}
echo $eudic_save

rm $shell_save
rm $clear_save
rm $md_save
rm $eudic_save
# # for i in `cat $file`
# for i in $(cat $file)
# do
#     j=$((j+1))
#     echo $j $i
# 	# wd $i >> $shell_save
# done
#-------------
cat $file | while read i
do
    j=$((j+1))
    echo $j $i
	wd $i >> $shell_save
done

cat mcc > $eudic_save   # 保存精简版 txt 格式，用于导入欧陆词典
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
