微雪(waveshare)指纹传感器
==========================

由于该指纹传感器需要串口通讯，目前而言并不太适合在基于ESP8266的NodeMCU上使用，因为ESP8266除了USB连接的UART0口，只提供了一个供TX的UART1口，并没有RX口。故而其实现很复杂。如确实想在8266版本的NodeMCU上使用，请查看源码自行修改。

将指纹传感器的电源线接好，将RX端接到SD3(GPIO10)，将TX端接到SD2(GPIO9)。

指纹录入::

    f = FINGER()
    f.add_finger()  # 运行后会要求连续按压3次指纹，返回True代表录入成功，False代表录入失败，可能是指纹上有异物，重试即可

已保存的指纹数量::

    f = FINGER()
    count = f.get_user_count()  # 已保存的指纹数量赋值给count变量

删除所有保存的指纹::

    f = FINGER()
    f.del_all_fingers()

匹配指纹::

    f = FINGER()
    f.match_finger()  # 如果当前指纹和已保存的指纹有相符的，会返回保存指纹的ID(ID必定>0)，否则返回0或False

