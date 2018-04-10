import time


class Finger():
    def __init__(self, ser):
        self.ser = ser
 
    # 添加指纹
    def add_finger(self, user_id=None):
        # 如果没有指定用户ID的话，就获取一个新的用户ID
        if not user_id:
            user_id = self.get_user_count() + 1
        # 由于该模块用户可以存储1000个指纹，然而一个字节只有8位，也就是只能存储256个指纹，所以需要2个字节来保存，第一个字节就叫做高8位，第二个字节就叫做低8位
        # 将用户id转变成高8位与低8位的形式
        low8 = user_id % (16 ** 2)
        high8 = int(user_id / (16 ** 2))
        # 该模块中，指纹添加的命令
        add_finger_cmd = [0xF5, 0x01, high8, low8, 1, 0, 0, 0xF5]
        print('Please Put Your Finger On Sensor...')
        result = self.send_cmd(add_finger_cmd)
        # 由于该模块要求指纹添加3次，故而需要判断3次
        if result == b'\xf5\x01\x00\x00\x00\x00\x01\xf5':
            add_finger_cmd[1] += 1
            print('Please Put Your Finger On Sensor Again...')
            result = self.send_cmd(add_finger_cmd)
            if result == b'\xf5\x02\x00\x00\x00\x00\x02\xf5':
                add_finger_cmd[1] += 1
                print('Please Put Your Finger On Sensor Again Again...')
                result = self.send_cmd(add_finger_cmd)
                if result == b'\xf5\x03\x00\x00\x00\x00\x03\xf5':
                    return True
        return False

    # 删除所有指纹
    def del_all_fingers(self):
        # 从指纹模块手册中查找到的删除指纹的命令
        cmd = [0xF5, 0x05, 0, 0, 0, 0, 0, 0xF5]
        # 生成检测位
        cmd = self.gen_chk(cmd)
        # 发送命令并获取返回值
        result = self.send_cmd(cmd)
        return result

    # 获取已登记的指纹数量
    def get_user_count(self):
        # 从指纹模块手册中查找到的获取已登记指纹数量的命令
        cmd = [0xF5, 0x09, 0, 0, 0, 0, 0, 0xF5]
        # 生成检测位
        cmd = self.gen_chk(cmd)
        # 发送命令并获取返回值
        result = self.send_cmd(cmd)
        return result[2] * (16 ** 2) + result[3]

    # 指纹匹配，如果正确返回user_id(从1开始)，否则返回False
    def match_finger(self):
        # 从指纹模块手册中查找到的指纹匹配的命令
        match_cmd = [0xF5, 0x0C, 0, 0, 0, 0, 0, 0xF5]
        # 生成检测位
        match_cmd = self.gen_chk(match_cmd)
        # 发送命令并获取返回值
        result = self.send_cmd(match_cmd)
        user_id = result[2] * (16 ** 2) + result[3]
        return user_id

    # 生成命令验真位
    def gen_chk(self, cmd):
        # 该指纹模块需要一个验证位，验证位为从第2位到第5位的或运算
        cmd[6] = cmd[1]
        for i in range(3, 6):
            cmd[6] = cmd[6] ^ cmd[i]  # 或运算为^
        return cmd

    # 发送命令
    def send_cmd(self, cmd):
        cmd = self.gen_chk(cmd)
        # 将命令从16进制转换成字节
        msg = bytes(cmd)
        print('sending: {}'.format(msg))
        # 发送到串口
        self.ser.write(msg)
        # 如果串口没有返回信息就一直等待
        try:
            while not self.ser.any():
                time.sleep(0.1)
        except Exception as e:
            while not self.ser.readable():
                time.sleep(0.1)
        # time.sleep(2)
        # 返回串口返回的8位信息
        if self.ser.any():
            result = self.ser.read(8)
        print(result)
        return result


if __name__ == '__main__':
    import serial
    ser = serial.Serial(port='COM5', baudrate=19200)
    finger = Finger(ser)
    print(finger.get_user_count())
    # finger.add_finger()