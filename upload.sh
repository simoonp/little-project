#!/bin/bash

# read -p "添加需要上传的文件(包括路径)" file

echo "需要上传的文件是： $@"

git add $@

echo "添加 commit"

read info
# read -p "添加 commit\n" info

git commit -m "$info"

git push origin main