# 导入时间库，这样可以使用等待的功能
import time


# 将针脚0作为数字输入
p = IN(0)


# 循环
@loop
def read_value():
    # 获取针脚0上输入的电平高低，如果为高则为1，如果为低则为0
    i = p.value()
    # 将其值打印出来
    print(i)
    # 等待1秒，防止刷新太快
    time.sleep(1)
