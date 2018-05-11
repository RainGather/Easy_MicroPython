__author__ = 'Qiu Cheng(Rain Gather)'
__email__ = 'raingather@outlook.com'
__project__ = 'https://github.com/RainGather/Easy_MicroPython'
__licence__ = 'GPL 3.0 https://github.com/RainGather/Easy_MicroPython/blob/release/LICENSE'

import time


class Finger():
    def __init__(self, send_ser, recv_ser=None, timeout=False):
        self.send_ser = send_ser
        if recv_ser is None:
            recv_ser = send_ser
        self.recv_ser = recv_ser
        self.add = self.add_finger
        self.delete = self.del_all_fingers
        self.count = self.get_user_count
        self.timeout = timeout
 
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
        self.send_cmd(add_finger_cmd)
        result = self.recv_cmd()
        while not result:
            result = self.recv_cmd()
        # 由于该模块要求指纹添加3次，故而需要判断3次
        if result == b'\xf5\x01\x00\x00\x00\x00\x01\xf5':
            add_finger_cmd[1] += 1
            print('Please Put Your Finger On Sensor Again...')
            self.send_cmd(add_finger_cmd)
            result = self.recv_cmd()
            while not result:
                result = self.recv_cmd()
            if result == b'\xf5\x02\x00\x00\x00\x00\x02\xf5':
                add_finger_cmd[1] += 1
                print('Please Put Your Finger On Sensor Again Again...')
                self.send_cmd(add_finger_cmd)
                # print('debug waiting')
                # time.sleep(3)
                result = self.recv_cmd()
                while not result:
                    result = self.recv_cmd()
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
        self.send_cmd(cmd)
        result = self.recv_cmd()
        while not result:
            result = self.recv_cmd()
        return result

    # 获取已登记的指纹数量
    def get_user_count(self):
        # 从指纹模块手册中查找到的获取已登记指纹数量的命令
        cmd = [0xF5, 0x09, 0, 0, 0, 0, 0, 0xF5]
        # 生成检测位
        cmd = self.gen_chk(cmd)
        # 发送命令并获取返回值
        self.send_cmd(cmd)
        result = self.recv_cmd()
        while not result:
            result = self.recv_cmd()
        return result[2] * (16 ** 2) + result[3]

    # 指纹匹配，如果正确返回user_id(从1开始)，否则返回False
    # def match_finger(self):
    #     # 从指纹模块手册中查找到的指纹匹配的命令
    #     match_cmd = [0xF5, 0x0C, 0, 0, 0, 0, 0, 0xF5]
    #     # 生成检测位
    #     match_cmd = self.gen_chk(match_cmd)
    #     # 发送命令并获取返回值
    #     result = self.send_cmd(match_cmd)
    #     if not result:
    #         return None
    #     user_id = result[2] * (16 ** 2) + result[3]
    #     return user_id

    # 生成命令验真位
    def gen_chk(self, cmd):
        # 该指纹模块需要一个验证位，验证位为从第2位到第5位的或运算
        cmd[6] = cmd[1]
        for i in range(3, 6):
            cmd[6] = cmd[6] ^ cmd[i]  # 或运算为^
        return cmd
    
    def ready_match(self):
        # 从指纹模块手册中查找到的指纹匹配的命令
        match_cmd = [0xF5, 0x0C, 0, 0, 0, 0, 0, 0xF5]
        # 生成检测位
        match_cmd = self.gen_chk(match_cmd)
        # 发送命令并获取返回值
        self.send_cmd(match_cmd, timeout=0.001)
        return True
    
    def match(self, timeout=1):
        result = self.recv_cmd()
        begin_time = time.time()
        while not result and time.time() - begin_time < timeout:
            result = self.recv_cmd()
        if result is not None:
            user_id = result[2] * (16 ** 2) + result[3]
            return user_id
        else:
            return None
    
    def recv_cmd(self):
        if self.recv_ser.any():
            result = self.recv_ser.read(8)
            print('recving: {}'.format(result))
        else:
            result = None
        return result

    # 发送命令
    def send_cmd(self, cmd, timeout=False):
        if not timeout:
            timeout = self.timeout
        cmd = self.gen_chk(cmd)
        # 将命令从16进制转换成字节
        msg = bytes(cmd)
        print('sending: {}'.format(msg))
        # 发送到串口
        self.send_ser.write(msg)
        return True
        # 如果串口没有返回信息就一直等待
        # if timeout:
        #     run_time = time.time()
        # try:
        #     while not self.read_ser.any():
        #         if timeout:
        #             if time.time() - run_time > timeout:
        #                 return None
        #         time.sleep(0.1)
        # except Exception as e:
        #     while not self.read_ser.readable():
        #         if timeout:
        #             if time.time() - run_time > timeout:
        #                 return None
        #         time.sleep(0.1)
        # # time.sleep(2)
        # # 返回串口返回的8位信息
        # if self.ser.any():
        #     result = self.ser.read(8)
        # else:
        #     return False
        # print(result)
        # return result


if __name__ == '__main__':
    import serial
    ser = serial.Serial(port='COM5', baudrate=19200)
    finger = Finger(ser)
    print(finger.get_user_count())
    # finger.add_finger()