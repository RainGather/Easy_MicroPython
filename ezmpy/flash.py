import os
import time
import pathlib
import sys
import subprocess


current_dir = os.path.split(os.path.realpath(__file__))[0]
os.chdir(current_dir)
current_path = pathlib.Path(current_dir)
mpfshell_py = os.path.join(current_dir, 'mpfshell.py')


try:
    import serial
    import colorama
    import websocket
except Exception as e:
    print(e, file=sys.stderr)
    print('未安装所需库，尝试自动安装中...(如安装失败请用管理员权限运行再试)')
    subprocess.call('pip install -r requirements.txt -i https://pypi.douban.com/simple', shell=True)
    print('安装结束，请关闭本窗口重新运行！(如安装失败请用管理员权限运行再试)')
    sys.exit()


def flash(com, main_file_name):
    print('尝试结束板子原先进程...')
    stop(com)
    print('刷入中，请等待，请不要断开连接，或断电，或对板子做任何操作，包括拔插线头，如长时间未反应，请直接关闭本窗口重试...')
    posix_d = current_path.as_posix()
    if ':' in posix_d:
        posix_d = posix_d.split(':')[1]
    cd_script = 'lcd \\"{}\\";'.format(posix_d)
    add_prefix(main_file_name)
    files = ['put \\"{}\\";'.format(p.name) for p in list(current_path.glob('*.py')) if p.name.lower() not in ['flash.py', 'api.py', 'mpfshell.py', 'windows.py']]
    mpf_script = ''.join(files)
    script = cd_script + mpf_script
    cmd = 'python "{}" --open {} -n -c \"{}\"'.format(mpfshell_py, com, script)
    print(cmd)
    p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = p.communicate()
    if 'not connected' in out.decode('utf-8', 'ignore').lower():
        return False
    return True


def add_prefix(main_file_name):
    main_file_path = current_path / '..' / main_file_name
    main_with_prefix = ''
    with main_file_path.open('r', encoding='utf-8') as fr:
        main_with_prefix = fr.read()
        lines = main_with_prefix.split('\n')
        if 'from ezmpy import *' not in lines:
            main_with_prefix = 'from ezmpy import *\n' + main_with_prefix
    with (current_path / 'main.py').open('w', encoding='utf-8') as fw:
        fw.write(main_with_prefix)
    return True


def find_com():
    for i in range(16):
        com = 'COM{}'.format(i)
        print('搜索中，尝试连接端口：{}'.format(com))
        cmd = 'python "{}" --open {} -n'.format(mpfshell_py, com)
        p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        try:
            info = p.communicate(timeout=3)[0].decode('utf-8', 'ignore').lower()
        except subprocess.TimeoutExpired:
            info = ''
        if 'connected' in info and 'not' not in info:
            print('找到端口号为： {}'.format(com))
            return com
        else:
            print('端口：{} 连接失败'.format(com))
    return False


# Maybe can not work too...
def stop(com):
    ser = serial.Serial(port=com, baudrate=115200, timeout=3)
    t = time.time()
    while not ser.writable() and time.time() - t < 10:
        pass
    ser.write('\x03'.encode('utf-8', 'ignore'))
    ser.close()


# Can not work...
def reboot(com):
    ser = serial.Serial(port=com, baudrate=115200, timeout=3)
    t = time.time()
    while not ser.writable() and time.time() - t < 10:
        pass
    ser.write('\x04'.encode('utf-8', 'ignore'))
    ser.close()


def repl(com):
    subprocess.call('python "{}" --open {} -c \"repl\"'.format(mpfshell_py, com), shell=True)


def get_main_file_name():
    files = [p.name for p in (current_path / '..').glob('*.py')]
    print('请选择烧录文件(如你想烧录的文件不在列表中，请将该文件复制到本目录下)：')
    for i in range(len(files)):
        print('[{}]: {}'.format(i, files[i]))
    i = input('请输入文件的序号(直接回车烧录main.py)：')
    if not i:
        return 'main.py'
    else:
        try:
            return files[int(i)]
        except Exception as e:
            print('输入错误！请关闭本窗口重试！')
            sys.exit()


if __name__ == '__main__':
    # main_file_name = input('请输入你想烧录的主程序文件名（请放置在本文件夹内，最好不要包括标点符号和空格，直接回车默认用main.py）：')
    # if not main_file_name:
    main_file_name = get_main_file_name()
    main_file_path = current_path / '..' / main_file_name
    if not (current_path / main_file_name).exists() and not main_file_path.exists():
        print('文件\"{}\"不存在本目录中，请仔细检查再运行！'.format(main_file_name))
        sys.exit()
    com = input('请输入COM端口号，可通过[WIN + X]快捷键，按[G]后，在设备管理器中查看，或者直接[回车]自动搜索： ')
    if not com:
        com = find_com()
        if not com:
            print('COM口没有找到！')
            sys.exit()
    if 'COM' not in com.upper():
        com = 'COM{}'.format(com)
    if flash(com, main_file_name):
        print('刷入成功！')
        reboot(com)
        print('')
        print('')
        print('')
        print('==========欢迎使用Assert驿站！==========')
        print('== 请按下主板上的重置[RST]按钮开始！  ==')
        print('== 请按下主板上的重置[RST]按钮开始！  ==')
        print('== 请按下主板上的重置[RST]按钮开始！  ==')
        print('========================================')
        print('')
        print('')
        print('')
        repl(com)
    else:
        print('刷入失败！请查看端口是否有被占用，可拔插后重试...')
        sys.exit()
