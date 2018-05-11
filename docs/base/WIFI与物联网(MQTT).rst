WiFi与物联网(MQTT)
=========================

用如下代码即可将NodeMCU连接至网络::

    wifi('wifiname', 'wifipwd')  # 请将内容改成自己的WiFi名和密码，注意不要有引号、中文等特殊字符，尽量纯英文+数字

连接网络后，即可使用urequests库，具体方法请查看 `urequests源代码 <https://github.com/micropython/micropython-lib/blob/master/urequests/urequests.py>`_

本项目已集成MQTT，可以方便的基于MQTT开发物联网设备。

MQTT是一种针对物联网优化过的协议，其结构很简单，为'主题-内容'对应式结构，下面用一个例子来说明：

假设C1是放置于机房的温度传感器物联网设备，C2是放置于办公室的机房过热报警灯。
那么C1可以发布一个主题，名为'computer_room/temperature'，值为当前温度。
C2可以订阅一个主题，名字与上述C1名一致。
这样一旦'computer_room/temperature'这个主题发生改变，C2就可以立刻获取改变后的值。获取值以后，可以判断其是否高于某个温度，从而决定是否发出警报。

默认情况下，一旦连接wifi，就会连接上test.mosquito.org的服务器，该服务器是公共服务器，如您只是测试使用，可用此服务器，如正式使用，请务必切换到安全的服务器。

用如下代码可以指定自己的MQTT服务器和验证方式::

    wifi('wifiname', 'wifipwd', False)  # 需要在连接WiFi时加入False参数，否则会直接连接到test.mosquito.org服务器。
    mqtt_init(host='www.yoursite.org', port=1883, user='yourusername', pwd='youruserpwd')  # 如果你的mqtt服务器没有验证，则可以不填写mqtt_user与mqtt_pwd

发布主题::

    pub('topic/can/split/like/path', 'str content')  # 注意必须使用str类型，如果是数字类型请自行转换

主题只能用英文，消息如果包含中文，需要进行编码::

    msg = '中文消息'
    pub('topic/can/split/like/path', msg.encode('utf-8'))

订阅主题，并设置触发后的操作::

    @sub('a/topic')  # 主题可以模糊订阅，用+表示一个级数，#表示多个级数
    def whatevername(topic, msg):  # 一旦订阅的主题发生改变，此函数就会接受发生改变的主题topic和消息msg
        # 接受到的topic和msg都是bytes类型，需要用decode转成字符串类型
        topic = topic.decode('utf-8')
        msg = msg.decode('utf-8')  
        print(topic, msg)
