import subprocess
import sys

from flash import find_com, mpfshell_py


if __name__ == '__main__':
    com = input('请输入COM端口号，可通过[WIN + X]快捷键，按[G]后，在设备管理器中查看，或者直接[回车]自动搜索： ')
    if not com:
        com = find_com()
        if not com:
            print('COM口没有找到！')
            sys.exit()
    if 'COM' not in com.upper():
        com = 'COM{}'.format(com)
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
    subprocess.call('python {} --open {} -c \"repl\"'.format(mpfshell_py, com), shell=True)