# git && github 使用记录

- 设置GitHub账户

```shell
$ git config --global user.name "GitHub用户名"
$ git config --global user.email "GitHub邮箱"
```

- 创建ssh-keygen

```shell
$ ssh-**key**gen -t rsa -b 4096 -C "github邮箱"
```

- 出现不再使用密码的错误

![Image](https://raw.githubusercontent.com/simoonp/picture/main/git_picture/set8.png)

在setting里

![Image](https://raw.githubusercontent.com/simoonp/picture/main/git_picture/set1.png)

![Image](https://raw.githubusercontent.com/simoonp/picture/main/git_picture/set2.png)

添加备注

![Image](https://raw.githubusercontent.com/simoonp/picture/main/git_picture/set3.png)

自己用的话可以把下面 **Select scopes** 全勾选上

![Image](https://raw.githubusercontent.com/simoonp/picture/main/git_picture/set4.png)

创建 Generate token

![Image](https://raw.githubusercontent.com/simoonp/picture/main/git_picture/set5.png)

复制token

![Image](https://raw.githubusercontent.com/simoonp/picture/main/git_picture/set6.png)

在 git push origin main 时使用token

![Image](https://raw.githubusercontent.com/simoonp/picture/main/git_picture/set7.png)

- 设置免密push

```shell
# 文件创建在用户主目录下：
touch .git-credentials
vim .git-credentials
https://{username}:{password}@github.com
# 添加 git config 内容
git config --global credential.helper store
# 执行此命令后，用户主目录下的.gitconfig 文件会多了一项：[credential]
# helper = store
# 重新 git push 就不需要用户名密码了。
```

![Image](https://raw.githubusercontent.com/simoonp/picture/main/git_picture/set9.png)

- push测试

```shell
# clone一个文件夹
git clone https://github.com/simoonp/little-project.git
# 创建一个空文件
touch git_github使用记录.md
# 将文件加入暂存区
git add git_github使用记录.md
# 提交文件，“”里面那是备注
git commit -m "提价空文档"
# 进行push
git push origin main
```

![Image](https://raw.githubusercontent.com/simoonp/picture/main/git_picture/push1.png)

