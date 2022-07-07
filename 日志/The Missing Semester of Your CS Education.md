# The Missing Semester of Your CS Education

B站视频链接：https://www.bilibili.com/video/BV1x7411H7wa

官网：https://missing.csail.mit.edu/ 

## 1、Shell

命令行提示符(shell prompt)

![image-20220419144555047](https://raw.githubusercontent.com/simoonp/upgit_picture/main/2022/04/upgit_20220419_1650350756.png)

`pwd` (present working directory)

![image-20220419145609561](https://raw.githubusercontent.com/simoonp/upgit_picture/main/2022/04/upgit_20220419_1650351369.png)

`cd` (change directory)

`.` 当前目录

`..` 上一层目录

`~` 用户目录

`-` 上一次的所在目录

`r`、`w`、`x`

`cp`、`mv`、`rm`、`rmdir`、`mkdir`

`man`(manual pages)

`Ctrl l`=`clear`

`stream`流

重定向流的方法：(默认的输出流是当前的终端)

`<` 重定向输入流

`>` 重定向输出流(复写 overwrite)

`cat`

`>>` 追加 append

`|`  管道 pipe：取程左边程序的输出作为右边程序的输入

`tail` 打印文件的最后几行 `tail [Option]... [File]...`

`sudo`

`xdg-open File` 选择一个合适的软件打开文件 

## 2、工具和脚本

shell变量

普通变量

字符串变量：

​	在字符串前后添加双引号`"`：可以解析字符串中的变量

​	在字符串前后添加双引号`'`：无法解析字符串中的变量

source 脚本，脚本中的函数会被加载到当前终端的环境中

脚本中的`$0`表示脚本的名称

`$?` 返回是一条命令的错误值，当命令正常执行时，返回值是`0`

`$_` 返回上条命令的最后一个参数

`!!` 返回上一条指令

`;` 连接中断中同一行的命令

`变量名=$(命令)` 将命令的结果存放到变量中

在脚本中，`$#` 的值是脚本参数的个数，`$$` 的值是本次脚本运行的`PID`，`$@` 展开所有的参数

![image-20220420224048555](https://raw.githubusercontent.com/simoonp/upgit_picture/main/2022/04/upgit_20220420_1650465648.png)

![image-20220420224058832](https://raw.githubusercontent.com/simoonp/upgit_picture/main/2022/04/upgit_20220420_1650465658.png)

通配符 `?` ，代替任何一个字符，通配符`*`，代替多个任意字符，`**`匹配零或多个目录名

`{ }` 内容展开

![无标题](https://raw.githubusercontent.com/simoonp/upgit_picture/main/2022/04/upgit_20220421_1650510438.png)

检查shell脚本语法是否准确——shellcheck

`tldr` 列出命令的简要示例 https://github.com/tldr-pages/tldr

`locate`  查找文件系统中具有指定子串的路径，`updatedb` 更新`located`的索引库，一般系统会定时更新

通过`grep` 查找文件内的指定内容：`grep -R "string" path`，`-R`递归`path`路径，`"string"`要查找的内容

类似功能的命令：`rg` 、`ripgrep` 

`history` 	结合`grep`；

`fzf` 模糊搜索指令

`tree`，`broot`(`tree`的升级版)，`nnn`(交互式的`tree`)

## 3、vim

![image-20220422111701318](https://raw.githubusercontent.com/simoonp/upgit_picture/main/2022/04/upgit_20220422_1650597421.png)

### `normal` 模式

```shell
x 删除当前光标字符
r-字符 替换光标内容为该字符

h 左	j 下	k 上	l 后	

b 移动到上一个单词 (background word)
w 移动到下一个单词 (word)
e 移动到单词末尾 (end)

0 移动到行首
$ 移动到行末
^ 移动到行首的第一个非空白字符

<C-u> 向上翻页
<C-d> 向下翻页

G 跳转到文件末
gg 跳转到文件首

L (low) 跳转到当前页面的最下面一行
M (middle) 跳转到当前页面的中间一行
H (high) 跳转到当前页面的最上面一行

f-字符 (find) 在当前行，向后查找，光标跳转到 第一次出现该字符的位置
F-字符 在当前行，向前查找，光标跳转到 第一次出现该字符的位置

t-字符 (to) 在当前行，向后查找，光标跳转到 第一次出现该字符的前面
T-字符 在当前行，向前查找，光标跳转到 第一次出现该字符的后面

i 切换到insert模式，光标不移动，然后输入数据会出现在光标前
a 切换到insert模式，光标向后移动一格，然后输入数据会出现在光标前
o 向下新开一空行，并在空行切换到insert模式
O 向上新开一空行，并在空行切换到insert模式

d 删除，一般配合 w、b、e使用；dw、db、de

c 改变，配合般配合 w、b、e使用，并在结束后加入insert模式，相当于 d 操作后键入i进入insert模式

一个指令连续使用两次，会作用于整行，dd 删除整行，cc 删除整行并进入insert模式

u (undo)撤销更改
<C-r> (redo)重做

y (yank)复制，y接受一个操作符作为参数
p (paste)粘贴，粘贴到光标后面
P (paste)粘贴，粘贴到光标前面

v (visual)切换到 普通visual模式，和普通文本编辑器的选中显示一样
V (visual-line)切换到 行visual模式，一次选中一行
<C-v> (visval-black)切换到 块visual模式，以矩形块的形式选中

~ 反转所选内容字母的大小写

数字-指令 重复执行指令，例如 4j、3dw...

% 在一对括号([]、())之间来回跳动
修饰符 a(around)、i(inside)
例如： da[ 删除接下来[..](包含[])的内容；di[ 删除接下来[..](不包含[])内的内容 (除了使用[ ( 还可以使用' " < 等其他成对出现的符号)

/字符串 搜索字符串
n 匹配下一个

. 重复上一次的操作，insert-操作-esc

<C-w>+方向键 切换窗格
```

### `insert` 模式

```shell

```

### `visval-black`模式
```shell
# 选中后，I 进入编辑模式
```


### `command-line` 模式

```shell
:sp	上下分屏
:^w	按默认顺序切换窗口
:^wj 切换到下面的窗口
:^wk 切换到上面的窗口
:qa	退出所有窗口

:set nu 显示行号
:行号 跳转到该行

:sp		# 上下分割窗口
:vsplit	# 左右分割窗口


```



`^V` <-->`Ctrl V`<-->`<C-V>`

`:q(uit)`

`:w`  

`:help`，例如`:help :w`

## 4、数据整理


`ssh` 指令

`less` 将文件内容分页显示

---

`sed` 流编辑器

`g` 尽可能多地执行操作

`正则表达式`

`^` 代表行首

`$`代表行未

`sed`默认支持地正则表达式是旧的格式，通过`-E`参数可以支持新的正则表达式格式

`捕获组`

比较完美的邮箱地址匹配 :`[Comparing E-mail Address Validating Regular Expressions (fightingforalostcause.net)](https://fightingforalostcause.net/content/misc/2006/compare-email-regex.php)`

---

`wc` 打印每个文件的换行符、单词和字节数；`-l` 统计行数

---

`sort`  支持多行输入，并排序输出

---

`uniq` 报告或省略重复的行

---

`awk` 基于列的流编辑器

默认使用空格分割列

---

`paste` 将输入的行汇总成一行，并默认使用`Tab`隔开

---

`bc`  计算器

`xargs` 将多行输入转换成参数，然后可以传递给程序或脚本

## 5、命令行环境

### 5.1 程序控制

`<C-z>` 暂停进程

`sleep` 休眠

`signal` 信号

`SIGSTOP` 暂停信号

`jobs` 列出当前终端(shell)的进程

`nohup` 用于在系统后台不挂断地运行命令，退出终端不会影响程序的运行 ` nohup Command [ Arg … ] [　& ]`；`nohup` 启动的程序不受`SIGHUP`信号影响

```shell
nohup Command [ Arg … ] [　& ]
Command：要执行的命令。

Arg：一些参数，可以指定输出文件。

&：让命令在后台执行，终端退出后命令仍旧执行。
```

`&` 在命令后加上`&`使指令后台运行

`bg` 恢复暂停的工作，并让工作在后台运行

`fg` 恢复暂停的工作，并让工作在前台运行

---

### 5.2 终端复用

`tmux`  (三个概念 会话(sessions)、窗口(标签)(Windows)、面板(panes) ) 

`tmux` 的进程和原始`shell`进程是分开的，只要`tmux`不关闭，原始`shell`关闭不影响`tmux`里的进程

**会话**

| 命令                                     | 功能                                      |
| ---------------------------------------- | ----------------------------------------- |
| tmux                                     | 新开一个会话(默认会话名称是从0开始的数字) |
| tmux new -s Name                         | 以指定名称开启新会话                      |
| tmux new -t Name                         | 复制Name名称的会话，两个会话共享数据      |
| tmux ls                                  | 列出当前所有会话                          |
| tmux a                                   | 重新连接最后一个会话                      |
| tmux a -t Name                           | 重新连接到指定会话                        |
| tmux rename-session -t old_name new_name | 重命名已创建的会话                        |



**窗口** (注：若在本地和远程同时使用`tmux`，需要确保远程的控制键(<C-b>)和本地的控制键不同，避免快捷键冲突，即远程和本地的`tmux`配置文件不同)

| 快捷键  | 功能                                  |
| ------- | ------------------------------------- |
| <C-b> d | 离开当前会话(先按 <C-b> 松开后在按 d) |
| <C-d>   | 关闭`tmux`                            |
| <C-b> c | 新开一个窗口                          |
| <C-b> N | 跳转到第N个窗口                       |
| <C-b> p | 切换到上一个窗口                      |
| <C-b> n | 切换到下一个窗口                      |
| <C-b> , | 重命名当前窗口                        |
| <C-b> w | 列出所有窗口                          |
|<C-b> Alt+<方向键> | 调节窗口大小 |

**面板**

| 快捷键          | 功能                                                         |
| --------------------- | ------------------------------------------------------------ |
| <C-b> "         | 向下分割(上下分割)                                           |
| <C-b> %         | 向右分割(左右分割)                                           |
| <C-b>  <方向键> | 切换到指定面板                                               |
| <C-b> z         | 切换当前面板的缩放(全屏/缩放当前面板)                        |
| <C-b> [         | 开始往回卷动屏幕。可以按下 <C-空格> 来开始选择，<Alt-w>键复制选中的部分（**注：在tmux的配置文件中将该模式配置成vi后，<空格>选中内容，<Shift-v>行选中mo'shi；<Enter>复制选中的数据，并滚动模式，详细快捷键参考：https://gist.github.com/ryerh/14b7c24dfd623ef8edc7 **） |
| <C-b> ]         | 粘贴缓冲区的数据                                             |
| <C-b> <空格>    | 切换面板布局                                                 |
| <C-b> x         | 关闭当前面板                                                 |


---

### 5.3 配置文件

**别名**:`alias 别名="别名代表的命令"` (注：`=`前后没有空格)

```shell
# 创建常用命令的缩写
alias ll="ls -lh"

# 能够少输入很多
alias gs="git status"
alias gc="git commit"
alias v="vim"

# 手误打错命令也没关系
alias sl=ls

# 重新定义一些命令行的默认行为
alias mv="mv -i"           # -i prompts before overwrite
alias mkdir="mkdir -p"     # -p make parent dirs as needed
alias df="df -h"           # -h prints human readable format

# 别名可以组合使用
alias la="ls -A"
alias lla="la -l"

# 在忽略某个别名
\ls
# 或者禁用别名
unalias la

# 获取别名的定义
alias ll
# 会打印 ll='ls -lh'

# bash 的 alias 不支持参数，可以通过定义函数的方式来传递参数
# alias 别名='函数名(){内容};函数名'
```

在默认情况下 shell 并不会保存别名。为了让别名持续生效，需要将配置放进 shell 的启动文件里，像是`.bashrc` 或 `.zshrc`.

### 5.4 远程控制

```shell
ssh 用户名@IP

ssh 用户名@IP 命令	# 在远程执行命令，并将命令的执行结果返回到本地

# ssh配置文件
```

`命令1 | tee 文件` 执行命令1，将结果显示到当前终端的同时把输出保存到文件中

传输文件

```shell
# scp

# rsync
```

## 6、版本控制(git)

```shell
# 初始化本地仓库
git init

# 检查当前git状态
git status

# 添加说明
git commit 

# 查看所有提交日志
git log
git log --all --graph --decorate
git log --all --graph --decorate --oneline # 显示更紧凑

# 将文件添加到缓存区
git add File

# 分支与合并
git branch	# 查看当前存储库的分支
git branch <name_of_new_branch>	# 创建新分支
git checkout <name_of_branch>	# 切换到另外一个分支
git checkout -b <name_of_new_branch> # 创建分支并切换到该分支
git merge <revision> # 将指定版本或分支，合并到当前分支
git mergetool # 使用工具来处理合并冲突
# 合并时，对于有的数据程序无法给出完美的合并结果，就需要手动合并；手动合并后，要重新git add，然后执行git merge --continue告诉git已经手动完成了合并

# 远程操作
git remote	# 列出远端
git remote add <name_of_rmeote> <name_of_url> # 添加一个远端, url除了是网上的存储库，还可以是本地文件夹路径
# git remote add origin path_name 	
# 远程仓库名字 “origin” 与分支名字 “master” 一样，在 Git 中并没有任何特别的含义一样。 同时 “master” 是当你运行 git init 时默认的起始分支名字，原因仅仅是它的广泛使用， “origin” 是当你运行 git clone 时默认的远程仓库名字。 如果你运行 git clone -o booyah，那么你默认的远程分支名字将会是 booyah/master。
git push <name_of_rmeote> <local_branch>:<remote_branch>	# 将本地分支推送到远端
git branch --set-upstream-to=<remote>/<remote branch> # 创建本地和远端分支的关联关系，指定后可以将简化git push指令
git fetch	# 从远端获取对象/索引， git fetch不会改变本地的内容
git pull <name_of_rmeote> <remote_branch> # 拉取远端
git clone # 从远端下载仓库

# 撤销
git commit --amend # 编辑提交的内容或信息
git reset HEAD <file> # 恢复暂存的文件
git checkout -- <file> # 丢弃修改

# 高级操作
~/.gitconfig # git配置
git clone --depth=1 # 浅克隆（shallow clone），不包括完整的版本历史信息
git add -p # 交互式暂存
git rebase -i # 交互式变基
git blame [<options>] [<rev-opts>] [<rev>] [--] <file># 查看最后修改某行的人
git stash # 暂时移除工作目录下的修改内容，恢复到最后一次提交的状态
git stash pop # 恢复刚刚的移除操作
git bisect # 通过二分查找搜索历史记录
.gitignore文件 # 在该文件内添加 指定不需要追踪的文件名
```

![image-20220426144944903](https://raw.githubusercontent.com/simoonp/upgit_picture/main/2022/04/upgit_20220426_1650957575.png)

绿色是本地分支，红色是远程分支

## 7、调试和分析

### 7.1 调试

`printf`

`log`

`/var/log` Linux系统存放日志的地方

`journalctl`

`pdb` 、`ipdb` python调试工具

```shell
python -m ipdb name.py

l # (list)列出代码
s # (step)逐步执行
c # (continue)
restart # 复位
p <变量名>	# 打印变量名
p local() # 打印目前的变量
q # (quit) 退出调试
b <N> # 在第N行设置断点
```

`gdb` 调试二进制文件(不仅仅是c)

```shell
```

`pyflakse` 、`mypy`静态分析工具

```shell
pyflakes name.py
mypy name.py
```

一些检查语法错误的插件

`writegoo` 检查英语语法

`Firefox`、`Chrome`调试网页

### 7.2 分析

**分析器**

分析那一段代码最耗资源，然后优先优化这块代码

跟踪分析器、采样分析器

`cProfile` python的分析器

`tac`与`cat`相反，反向输出数据

`memory_profiler` python的内存分析器

`Valgrind` C内存分析器

`perf` 

`FlameGraph` 采样分析器

调用图

`htop` 

`du` 查看文件磁盘占用

`ncdu` 交互式查看文件的磁盘占用

`losf` 查看哪个进程在占用文件

`hyperfine` 比较两个程序的速度

## 8、元编程

`make`

`apt`

软件版本：`主版本号.次版本号.补丁号`。

```
如果新的版本没有改变 API，请将补丁号递增；
如果您添加了 API 并且该改动是向后兼容的，请将次版本号递增；
如果您修改了 API 但是它并不向后兼容，请将主版本号递增。
```

`测试套件`：所有测试的统称

`单元测试`：一种“微型测试”，用于对某个封装的特性进行测试。

测试单个功能

`集成测试`：一种“宏观测试”，针对系统的某一大部分进行，测试其不同的特性或组件是否能*协同*工作。

`回归测试`：一种实现特定模式的测试，用于保证之前引起问题的 bug 不会再次出现。

`模拟（Mocking）`: 使用一个假的实现来替换函数、模块或类型，屏蔽那些和测试不相关的内容。例如，您可能会“模拟网络连接” 或 “模拟硬盘”。

...

## 9、安全和密码学

## 10、大杂烩

10.1、按键映射

10.2、守护进程

10.3、FUSE(用户空间文件系统)

允许运行在用户空间上的程序实现文件系统调用，并将这些调用与内核接口联系起来

10.4、备份

`复制存储`在同一个磁盘上的数据不是备份，因为这个磁盘是一个单点故障（single point of failure）

推荐的做法是将数据备份到不同的地点存储。

`同步方案`也不是备份。即使方便如 Dropbox 或者 Google Drive，当数据在本地被抹除或者损坏，同步方案可能会把这些“更改”同步到云端。同理，像 RAID 这样的磁盘镜像方案也不是备份。它不能防止文件被意外删除、损坏、或者被勒索软件加密。

`有效备份方案`的几个核心特性是：版本控制，删除重复数据，以及安全性。

10.5、API(应用程序接口)

10.6、常见命令行标志参数及模式

```shell
--help # 

# 会造成不可撤回操作的工具一般会提供“空运行”（dry run）标志参数，这样用户可以确认工具真实运行时会进行的操作。

--version 或者 -V # 显示它的版本信息

-vvv # 让工具输出更详细的信息（经常用于调试）

--quiet # 抑制除错误提示之外的其他输出。

- # 使用 - 代替输入或者输出文件名意味着工具将从标准输入（standard input）获取所需内容，或者向标准输出（standard output）输出结果。

# 会造成破坏性结果的工具一般默认进行非递归的操作，但是支持使用“递归”（recursive）标志函数（通常是 -r）。

-- # 特殊参数 -- 让某个程序 停止处理 -- 后面出现的标志参数以及选项（以 - 开头的内容）
```

10.7、窗口管理器

10.8、VPN

10.9、Markdown

10.10、桌面自动化

[Hammerspoon](https://www.hammerspoon.org/) 是面向 macOS 的一个桌面自动化框架。它允许用户编写和操作系统功能挂钩的 Lua 脚本，从而与键盘、鼠标、窗口、文件系统等交互。

10.11、Docker, Vagrant, VMs, Cloud, OpenStack

10.12、交互式记事本编程

10.13、GitHub

## 11、提问&回答

