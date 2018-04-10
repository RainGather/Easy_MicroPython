import os
import sys
import pathlib
import subprocess


try:
    from mp import mpfshell
except Exception as e:
    print('Can not found mpfshell, try install...')
    subprocess.call('pip install mpfshell')
    print('Install done, please restart and try again.')
    sys.exit()
    

# current_dir = os.path.split(os.path.realpath(__file__))[0]
current_path = pathlib.Path('.')
os.chdir(current_path)
LIB_NAME = 'ezmpy'


def flash(com):
    print('刷入中，请等待，请不要断开连接，或断电，或对板子做任何操作，包括拔插线头，如长时间未反应，请直接关闭本窗口重试...')
    posix_d = current_path.as_posix()
    if ':' in posix_d:
        posix_d = posix_d.split(':')[1]
    lcd_script = 'lcd \\"{}\\";'.format(posix_d)
    cd_script = 'mk {}; cd {};'.format(LIB_NAME, LIB_NAME)
    files = ['put \\"{}\\";'.format(p.name) for p in list((current_path / LIB_NAME).glob('*.py'))]
    mpf_script = ''.join(files)
    script = lcd_script + cd_script + mpf_script
    cmd = 'python -m mp.mpfshell --open {} -n -c \"{}\"'.format(com, script)
    print(cmd)
    p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = p.communicate()
    if 'not connected' in out.decode('utf-8', 'ignore').lower():
        return False
    return True


def find_com():
    for i in range(16):
        com = 'COM{}'.format(i)
        print('搜索中，尝试连接端口：{}'.format(com))
        cmd = 'python -m mp.mpfshell --open {} -n'.format(com)
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
    


if __name__ == '__main__':
    com = input('请输入COM端口号，可通过[WIN + X]快捷键，按[G]后，在设备管理器中查看，或者直接[回车]自动搜索： ')
    if not com:
        com = find_com()
        if not com:
            print('COM口没有找到！')
            sys.exit()
    if 'COM' not in com.upper():
        com = 'COM{}'.format(com)
    if flash(com):
        print('刷入成功！')
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
    else:
        print('刷入失败！请查看端口是否有被占用，可拔插后重试...')
        sys.exit()
        