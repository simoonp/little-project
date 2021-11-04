#!/bin/bash
sed '/2021/d;/^\s*$/d' $1 > mcc
#data=$(cat temp)
file="mcc"
echo "------"
j=0
save="c"$1
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

sed -i 's/\[31m//' $save
sed -i 's/\[32m//' $save
sed -i 's/\[33m//' $save
sed -i 's/\[0m//' $save
sed -i 's/\[36m//' $save
sed -i 's/\[34m//' $save
sed -i 's/\[36m//' $save
sed -i 's/\[31m//' $save
sed -i 's/\[0m//' $save
sed -i 's///' $save
sed -i 's///' $save
sed -i 's///' $save
sed -i 's///' $save

sed -i G $save  # 添加空行
