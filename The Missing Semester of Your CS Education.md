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

`normal` 模式

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
```

`insert` 模式

```shell

```



`command-line` 模式

```shell
:sp	上下分屏
:^w	按默认顺序切换窗口
:^wj 切换到下面的窗口
:^wk 切换到上面的窗口
:qa	退出所有窗口

:set nu 显示行号
:行号 跳转到该行
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

**面板**

| 快捷键          | 功能                                                         |
| --------------- | ------------------------------------------------------------ |
| <C-b> "         | 向下分割(上下分割)                                           |
| <C-b> %         | 向右分割(左右分割)                                           |
| <C-b>  <方向键> | 切换到指定面板                                               |
| <C-b> z         | 切换当前面板的缩放(全屏/缩放当前面板)                        |
| <C-b> [         | 开始往回卷动屏幕。可以按下 <C-空格> 来开始选择，<Alt-w>键复制选中的部分 |
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



