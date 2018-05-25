import sys
import time
import subprocess
import pathlib
try:
    import serial
    from mp import mpfshell
except Exception as e:
    print('未安装pyserial或mpfshell，尝试安装中...')
    subprocess.check_call('pip install pyserial mpfshell -i https://pypi.douban.com/simple', shell=True)
    print('安装成功！请关闭本窗口重新运行。')
    sys.exit()


def get_coms():
    coms = []
    for i in range(20):
        com = 'COM' + str(i)
        try:
            s = serial.Serial(com, 9600, timeout=1)
            s.close()
            coms.append(com)
        except serial.SerialException:
            pass
    return coms


def wipe(com):
    print('清空NodeMCU中...')
    subprocess.check_call('python esptool.py --port {} --baud 9600 erase_flash'.format(com), shell=True)
    print('NodeMCU已清空！')


def flash_micropython(com, chip):
    print('刷入MicroPython中...')
    if chip == 'ESP8266':
        subprocess.check_call('python esptool.py --port {} --baud 460800 write_flash --flash_size=detect -fm dio 0 esp8266-20171101-v1.9.3.bin'.format(com), shell=True)
    if chip == 'ESP32':
        subprocess.check_call('python esptool.py --chip esp32 --port {} write_flash -z 0x1000 esp32-20180408-v1.9.3-521-gd6cf5c67.bin'.format(com), shell=True)
    print('MicroPython框架已刷入！')


def flash_ezmpy(com):
    print('刷入Easy MicroPython中...')
    LIB = 'ezmpy'
    current_path = pathlib.Path('.')
    posix_d = (current_path / LIB).absolute().as_posix()
    if ':' in posix_d:
        posix_d = posix_d.split(':')[1]
    lcd_script = 'lcd \\"{}\\";'.format(posix_d)
    files = ['put \\"{}\\";'.format(p.name) for p in list((current_path / LIB).glob('*py'))]
    mpf_script = ''.join(files)
    scripts = lcd_script + mpf_script
    subprocess.check_call('python -m mp.mpfshell --open {} -n -c \"{}\"'.format(com, scripts), shell=True)
    print('刷入成功！')


def main():
    coms = get_coms()
    com = input('当前可用的串口有：{}\n请输入想烧录的COM口:'.format(' '.join(coms)))
    if not com:
        com = coms[0]
    chip = input('芯片是ESP8266还是ESP32(输入ESP8266或ESP32):')
    if not chip:
        chip = 'ESP8266'
    wipe(com)
    time.sleep(1)
    flash_micropython(com, chip.upper())
    print('端口冷却中，请勿关闭窗口或拔出设备，请等待...')
    time.sleep(5)
    flash_ezmpy(com)


if __name__ == '__main__':
    main()
