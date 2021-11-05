#!/bin/bash
sed '/2021/d;/^\s*$/d' $1 > mcc
#data=$(cat temp)
file="mcc"
echo "------"
j=0
save="s"$1
for i in $(cat $file)
do
    j=$((j+1))
    echo $j
    #data=$(wd $i)
	wd $i >> $save
	#wd $data >> $save
    echo $data
done
rm mcc

# 一下格式方便终端显示
# sed -i 's/\[31m//' $save
# sed -i 's/\[31m//' $save
# sed -i 's/\[32m//' $save
# sed -i 's/\[33m//' $save
# sed -i 's/\[0m//' $save
# sed -i 's/\[36m//' $save
# sed -i 's/\[34m//' $save
# sed -i 's/\[36m//' $save
# sed -i 's/\[31m//' $save
# sed -i 's/\[0m//' $save
# sed -i 's///' $save
# sed -i 's///' $save
# sed -i 's///' $save
# sed -i 's///' $save
# s
# sed -i G $save  # 添加空行

# 以下方便md格式查看
sed -i 's/\[31m/<font color=Red>/' $save	# 将终端红色转换为md红色
sed -i 's/\[31m/<font color=Red>/' $save	
sed -i 's/\[31m/<font color=Red>/' $save	
sed -i 's/\[32m/<font color=Green>/' $save	# 将终端绿色转换为md绿色	
sed -i 's/\[33m/<font color=Yellow>/' $save	# 将终端黄色转换为md黄色
sed -i 's/\[34m/<font color=Blue>/' $save	# 将终端蓝色转换为md蓝色
sed -i 's/\[36m/<font color=Teal>/' $save	# 将终端蓝绿色转换为md蓝绿色
sed -i 's/\[36m/<font color=Teal>/' $save
sed -i 's/\[36m/<font color=Teal>/' $save

sed -i 's/\[0m/<\/font>/' $save	# 匹配<font>标志
sed -i 's/\[0m/<\/font>/' $save

sed -i 's///' $save
sed -i 's///' $save
sed -i 's///' $save
sed -i 's///' $save

sed -i G $save  # 添加空行
