LED闪烁
===========

将LED连接到针脚0，随后可以用如下代码控制::

    # 导入time库，可以使用等待等功能
    import time


    # 设置针脚0为输出端
    p = OUT(0)


    while True:
        # 将针脚0设为高电平，这样连接针脚0的LED灯就会发光
        p.on()
        # 等待1秒
        time.sleep(1)
        # 将针脚0设为低电平，这样连接针脚0的LED灯就会灭了
        p.off()
        # 等待1秒
        time.sleep(1)
