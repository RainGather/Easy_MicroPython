串口MQTT控制
==================

连接Wifi::

    wif|wifiname|wifipwd;

设定服务器(默认为test.mosquitto.org)::

    svr|test.mosquitto.org|1883|user|pwd;

其中端口号、用户名和密码可以为空。

订阅主题::

    sub|title/subtitle;

主题有消息时会返回一条消息(请自行完成监听)::

    sub|title/subtitle|[msg];

发送消息::

    pub|title/subtitle;

以上命令都会在成功执行后返回::

    sta|ok;

如需重启或重置，可以发送命令::

    sys|reboot;

会收到命令::
    
    sys|rebooting;
