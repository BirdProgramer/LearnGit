# ʹ��shadowsocksʵ�ֿ�ѧ����
������˹���ķ������������ſ�ѧ���������˺ܶ�̳̣����վ�����shadowsocks���ҵ�ϵͳ��ubuntu16.04������������¡�

### ��װshadowsocks
Linux��ͬ�ķ��а�ִ�е��������£�
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
��װ��ɺ�����ssserver --version �鿴�汾���� ssserver -h �鿴������������ͼ��ʾ��˵����װ�ɹ��ˡ�
### ����
���������÷�ʽ��һ���������з�ʽ��һ�������ļ���ʽ��

 - �����з�ʽ
	ͨ�� ssserver -h ���Կ����ܶ�����������塣�������£�
	```
	ssserver -s "server_ip" -p port -k "password" -m "rc4-md5" -t 300
	```
	���У�server_ip��Ϊ��ķ�����IP��ַ��port��Ϊ��Ķ˿ڣ�����˿�>10000��,password��Ϊ������룬rc4-md5Ϊ���µļ��ܷ�ʽ��300Ϊ��ʱʱ�䡣
 - �����ļ���ʽ
   �½�config.json�ļ���Ŀ¼������ѡ������Ҫ��ס��,�༭����Ϊ��
   ```
   {
	    "server":"��������ip",                 #��Ϊ��������IP
	    "server_port":19175,                   #���Ը�Ϊ����˿ڣ��������10000�������ͻ
	    "local_address":"127.0.0.1",
	    "local_port":1080,
	    "password":"����",                     #��������
	    "timeout":300,
	    "method":"aes-256-cfb",             #���ܷ�ʽ
	    "fast_open":false
}
```
��������� ssserver -c config.json ������������
### ��������
ĿǰΪֹ�������������ˣ����ǵ���ر��նˣ������������������������ֹ�ˣ���Ҫ��������ˣ���Ҫ���÷�����̱�Ϊ��̨�����Լ�����������

 -  ��̨����
	linux�У�nohup ��ʾ�������йҶ��źţ�& ��ʾ��̨���У��޸ĺ������Ϊ��
	```
	nohup ssserver -s "server_ip" -p port -k "password" -m "rc4-md5" -t 300 &
	```
	����
	```
	nohup ssserver -c config.json &
	```
	��ʱ��ϵͳ����ʾ���������Ĭ�������nohup.out�ļ��ڡ�
 - ��������
  �½�һ��shadow.sh�ļ���д���������ݡ�
	  ```
	  #��/bin/bash
      #  shadow.sh
      nohup ssserver -c /root/config.json &          #����config.jsonҪд����·��
	  ```
  /etcĿ¼�µ�rc.local�ű���һ��Ubuntu��������Զ�ִ�еĽű������Ǵ򿪸��ļ���exit֮ǰ����
  ```
  nohup bash /root/shadow.sh>/home/d.txt &         #�����shadow.sh Ҫд����·��
  ```
  ��ɺ󱣴档ע�⣬�༭rc.local�ļ���ҪrootȨ�ޡ�
���ˣ�������Ѿ���������ˡ�
### �ͻ���

 - windows
	 [�������ء�](https://github.com/shadowsocks/shadowsocks-windows/releases)��ɺ��ѹ��˫��Shadowsocks.exe���õ�����
	 ��֮ǰ��������Ϣ���룬��ɺ���ȷ��������ɿͻ������á�
 - ��׿
 [��������](https://github.com/shadowsocks/shadowsocks-android/releases)����ɺ�װ���༭�����ļ�����֮ǰ��������Ϣ���뼴�ɡ�

���ˣ����Ǳ�ʵ���˿�ѧ�������Ͽ����԰ɡ�
