# 连接网络
wifi('WiFiName', 'WiFiPassWord')


# 声明0针脚为数字输出
p = OUT(0)


# 当云变量btn的值变成down时，会运行函数内的代码。函数名可以随意取，变量btn的名字需要与云端设置的名字一致
@when(btn='down')
def down():
    # 将针脚的输出变成高电平，也就是通电。这样0针脚接着的LED灯就亮了
    p.on()


# 当云变量btn的值变成up时，会运行函数内的代码。函数名可以随意取，变量btn的名字需要与云端设置的名字一致
@when(btn='up')
def up():
    # 将针脚的输出变成低电平，也就是断电。这样0针脚接着的LED灯就灭了
    p.off()
