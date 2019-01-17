# djangoproject
git基本概念:
工作区：就是你在电脑里能看到的目录。
暂存区：英文叫stage, 或index。一般存放在 ".git目录下" 下的index文件（.git/index）中，所以我们把暂存区有时也叫作索引（index）。
版本库：工作区有一个隐藏目录.git，这个不算工作区，而是Git的版本库。

git环境配置:
在Linux Ubuntu16.04下安装git: sudo apt-get install git-core
配置个人的用户名称和电子邮件地址：
$ git config --global user.name "用户名"
$ git config --global user.email "邮箱地址"

创建github账号
创建远程仓库
公钥认证管理
从远程库克隆:git clone <仓库地址>

在本地项目中完成开发后先add提交至本地暂存区
git add 文件1 文件2 ...
git add 目录
git add .

在本地暂存区commit提交至本地仓库
git commit -m '本次提交的说明信息'

把当前项目推送至push远程仓库进行更新
git push origin master

查看暂存区的状态
git status