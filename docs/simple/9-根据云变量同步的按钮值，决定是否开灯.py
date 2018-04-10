wifi('WiFiName', 'WiFiPassWord')


# 将针脚0作为数字输出，连接LED灯
p = OUT(0)


# 当button云变量变成1时，就会开灯
@when(button='1')
def led_on():
    p.on()

# 当button云变量变成0时，就会灭灯
@when(button='0')
def led_off():
    p.off()
