PWM输出
===========

PWM为脉冲宽度调制输出，可以理解成释放出最高电压一定百分比的电压。
并不是所有的针脚都支持PWM输出，其中

:ESP8266: 针脚D0, 2, 4, 5, 12, 13, 14 和 15支持PWM模拟输出

:ESP32: GPIOs 0, 1, 2, 3, 4, 5, 12, 13, 14, 15, 16, 17, 18 ,19, 21, 22, 23, 25, 26, 27, 32, 33支持

MicroPython中，PWM的范围为0-1023.

可以用如下代码来产生PWM::

    p = PWM(2)  # 2针脚用于PWM输出
    p.duty(512)  # 占空比设置为512/1024

