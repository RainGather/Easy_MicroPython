微雪(waveshare)指纹传感器
==========================

由于该指纹传感器需要串口通讯，目前而言并不太适合在基于ESP8266的NodeMCU上使用，因为ESP8266除了USB连接的UART0口，只提供了一个供TX的UART1口，并没有RX口。故而其实现很复杂。如确实想在8266版本的NodeMCU上使用，请查看源码自行修改。

将指纹传感器的电源线接好，将RX端接到SD3(GPIO10)，将TX端接到SD2(GPIO9)。

声明对象::

    f = FINGER()

如需设定超时，用如下方式声明::

    f = FINGER(timeout=10)  # 将FINGER换成ZHIWEN也同效果

指纹录入::

    f.add()  # 运行后会要求连续按压3次指纹，返回True代表录入成功，False代表录入失败，可能是指纹上有异物，重试即可

已保存的指纹数量::

    count = f.count()  # 已保存的指纹数量赋值给count变量

删除所有保存的指纹::

    f.delete()

匹配指纹::

    f.match_finger()  # 如果当前指纹和已保存的指纹有相符的，会返回保存指纹的ID(ID必定>0)，否则返回0或False

由于指纹匹配时，处于阻塞状态，无法进行任何其它操作，故而可以人工异步匹配::

    import time

    f = FINGER()
    f.ready()  # 指纹模块进入识别状态
    while True:
        result = f.match()
        if result == 0:
            print('Finger Error!')  # 匹配错误，指纹不是已录入指纹
            f.ready()  # 重新进入识别状态进行比对
        if result is None:
            print('Waiting for Finger!')  # 指纹还处于识别状态，还没有手指放上去让识别
        if result:
            print('Right!')
        time.sleep(0.1)
