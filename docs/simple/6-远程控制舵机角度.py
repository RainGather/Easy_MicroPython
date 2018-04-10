# 连接WiFi
wifi('WiFiName', 'WiFiPassWord')


# 声明2针脚连接舵机的信号线，针脚0, 2, 4, 5, 12, 13, 14 和 15支持舵机控制，如舵机不是50HZ的，可以用Duoji(2, freq=频率)的方式来声明
duoji = Duoji(2)


# 当云变量jiaodu的值发送变化时，会把jiaodu的值赋给函数中的v，并运行函数内的代码。函数名可以随意取，变量jiaodu的名字需要与云端设置的名字一致
@when('jiaodu')
def down(v):
    # 由于获取到的云变量都是字符串，需要用int将其转成整数
    v = int(v)
    # 将舵机旋转v度，普通舵机理论上可以转0-180度，但由于舵机制作的精度原因，建议控制在30-150度左右旋转
    duoji.turn(v)
