# 使用shadowsocks实现科学上网
最近租了国外的服务器，便想着科学上网，搜了很多教程，最终决定用shadowsocks，我的系统是ubuntu16.04，具体过程如下。

### 安装shadowsocks
Linux不同的发行版执行的命令如下：
Debian / Ubuntu:
```
apt-get install python-pip
pip install shadowsocks
```
CentOS:
```
yum install python-setuptools && easy_install pip
pip install shadowsocks
```
安装完成后，输入ssserver --version 查看版本或者 ssserver -h 查看帮助，出现下图所示，说明安装成功了。
### 配置
有两种配置方式，一种是命令行方式，一种配置文件方式。

 - 命令行方式
	通过 ssserver -h 可以看到很多参数及其意义。命令如下：
	```
	ssserver -s "server_ip" -p port -k "password" -m "rc4-md5" -t 300
	```
	其中，server_ip改为你的服务器IP地址，port改为你的端口（建议端口>10000）,password改为你的密码，rc4-md5为最新的加密方式，300为超时时间。
 - 配置文件方式
   新建config.json文件（目录可以任选，但是要记住）,编辑内容为：
   ```
   {
	    "server":"服务器的ip",                 #改为服务器的IP
	    "server_port":19175,                   #可以改为任意端口，建议大于10000，避免冲突
	    "local_address":"127.0.0.1",
	    "local_port":1080,
	    "password":"密码",                     #设置密码
	    "timeout":300,
	    "method":"aes-256-cfb",             #加密方式
	    "fast_open":false
}
```
保存后，输入 ssserver -c config.json 即可启动服务。
### 开机自启
目前为止，服务是启动了，但是当你关闭终端，或者重启服务器，服务便终止了，需要重启，因此，需要将该服务进程变为后台运行以及开机启动。

 -  后台运行
	linux中，nohup 表示忽略所有挂断信号，& 表示后台运行，修改后的命令为：
	```
	nohup ssserver -s "server_ip" -p port -k "password" -m "rc4-md5" -t 300 &
	```
	或者
	```
	nohup ssserver -c config.json &
	```
	此时，系统会提示进程输出会默认输出到nohup.out文件内。
 - 开机自启
  新建一个shadow.sh文件，写入如下内容。
	  ```
	  #！/bin/bash
      #  shadow.sh
      nohup ssserver -c /root/config.json &          #这里config.json要写绝对路径
	  ```
  /etc目录下的rc.local脚本是一个Ubuntu开机后会自动执行的脚本，我们打开改文件，exit之前加上
  ```
  nohup bash /root/shadow.sh>/home/d.txt &         #这里的shadow.sh 要写绝对路径
  ```
  完成后保存。注意，编辑rc.local文件需要root权限。
至此，服务端已经配置完成了。
### 客户端

 - windows
	 [请先下载。](https://github.com/shadowsocks/shadowsocks-windows/releases)完成后解压，双击Shadowsocks.exe，得到如下
	 将之前的配置信息填入，完成后点击确定即可完成客户端配置。
 - 安卓
 [请先下载](https://github.com/shadowsocks/shadowsocks-android/releases)，完成后安装，编辑配置文件，将之前的配置信息填入即可。

至此，我们便实现了科学上网，赶快试试吧。
