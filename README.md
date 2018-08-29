# Hi-Loggin
HIT-Loggin
哈尔滨工业大学校园网认证脚本Python版

（原GUI版本重构，暂不提供）

###支持平台

Linux

Windows
请先安装Python3.5及以上版本并安装requests库，在Ubuntu上可执行
> sudo apt install python3 python3-pip
> pip3 install requests


###使用方法(Linux为例)
1. 下载脚本
> git clone https://github.com/hit-hanbo/Hi-Loggin.git
2. 建立配置文件
> touch Hi-Loggin/login.cfg
按照以下格式填写账号密码
> 用户名:密码，例如：
> 1234567890:12345
3. 连接校园网
> python3 Login.py auto #自动连接
> python3 Login.py manual #手动连接
> python3 Login.py logout #注销


###说明
模块支持二次开发，如开发GUI系统


hithanbo@gmail.com
