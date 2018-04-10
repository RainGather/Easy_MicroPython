import time


# 2针脚连DHT11温湿度传感器的数据端
d = DHT11(2)


@loop
def temp():
    # 一口气获取温度和湿度
    wendu, shidu = d.get()
    # 打印温度到窗口
    print(wendu)
    # 打印湿度到窗口
    print(shidu)
    # 等待1秒
    time.sleep(1)
