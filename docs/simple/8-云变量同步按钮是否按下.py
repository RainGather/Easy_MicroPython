wifi('WiFiName', 'WiFiPassWord')


# 将针脚0作为数字输入
p = IN(0)


# 绑定变量，button为随意设置的变量名，不过请保持所有地方一致
@sync('button')
def read_value():
    # 获取针脚0上输入的电平高低，如果为高则为1，如果为低则为0
    i = p.value()
    # 将针脚0获取的值，绑定到button云变量中。这样云变量button就会保持和针脚0的值同步
    return i
