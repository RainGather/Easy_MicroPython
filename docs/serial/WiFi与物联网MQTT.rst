串口MQTT控制
==================


注意！！！！！！
==================
串口模式一定要使用5V供电，3.3V的供电会导致串口出问题最终影响使用！！！！


再注意！！！！！！！
==================
发送命令时，请等待几秒，例如连接好WiFi后，请等待5秒再发送下一个命令。否则可能导致命令被忽略！


连接Wifi::

    [wif|wifiname|wifipwd]

如果WiFi连接错误会自动退出，返回::

    [sta|exit]

设定服务器(默认为test.mosquitto.org，你可以自行搭建一个服务器，也可以使用他人的服务器，例如：https://www.cloudmqtt.com/，需注册)::

    [svr|test.mosquitto.org|1883|user|pwd]

其中端口号、用户名和密码可以为空::

    [svr|test.mosquitto.org]
    [svr|test.mosquitto.org|1883]

订阅主题::

    [sub|title/subtitle]

主题有消息时会返回一条消息(请自行完成监听)::

    [sub|title/subtitle|msg]

发送消息::

    [pub|title/subtitle|msg]

以上命令都会在成功执行后返回::

    [sta|ok]

如需重启或重置，可以发送命令::

    [sys|reboot]

会收到命令::
    
    [sys|rebooting]


手机端MQTT连接推荐: https://apkpure.com/linear-mqtt-dashboard/com.ravendmaster.linearmqttdashboard
