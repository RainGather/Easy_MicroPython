WiFi联网
=============

用如下代码即可将NodeMCU连接至网络::

    WIFI('wifiname', 'wifipwd')  # 请将内容改成自己的WiFi名和密码，注意不要有引号、中文等特殊字符，尽量纯英文+数字

连接网络后，即可使用urequests库，具体方法请查看 `urequests源代码 <https://github.com/micropython/micropython-lib/blob/master/urequests/urequests.py>`_
