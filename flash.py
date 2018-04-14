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


def flash(com, file=None):
    print('刷入中，请等待，请不要断开连接，或断电，或对板子做任何操作，包括拔插线头，如长时间未反应，请直接关闭本窗口重试...')
    posix_d = (current_path / LIB_NAME).absolute().as_posix()
    if ':' in posix_d:
        posix_d = posix_d.split(':')[1]
    lcd_script = 'lcd \\"{}\\";'.format(posix_d)
    # cd_script = 'md {}; cd {};'.format(LIB_NAME, LIB_NAME)
    cd_script = ''
    if file:
        print('刷入文件{}中...'.format(file))
        add_prefix(file)
        print('更新Easy MicroPython框架中...')
    else:
        if (current_path / LIB_NAME / 'main.py').exists():
            os.remove(current_path / LIB_NAME / 'main.py')
        print('刷入Easy MicroPython框架中...')
    files = ['put \\"{}\\";'.format(p.name) for p in list((current_path / LIB_NAME).glob('*.py'))]
    mpf_script = ''.join(files)
    script = lcd_script + cd_script + mpf_script
    cmd = 'python -m mp.mpfshell --open {} -n -c \"{}\"'.format(com, script)
    # print(cmd)
    p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = p.communicate()
    if 'not connected' in out.decode('utf-8', 'ignore').lower():
        return False
    return True
    

def repl(com):
    subprocess.call('python -m mp.mpfshell --open {} -c \"repl\"'.format(com), shell=True)


def add_prefix(main_file_name):
    main_file_path = current_path / main_file_name
    main_with_prefix = ''
    with main_file_path.open('r', encoding='utf-8') as fr:
        main_with_prefix = fr.read()
        lines = main_with_prefix.split('\n')
        if 'from ezmpy import *' not in lines:
            main_with_prefix = 'from ezmpy import *\n' + main_with_prefix
    with (current_path / LIB_NAME / 'main.py').open('w', encoding='utf-8') as fw:
        fw.write(main_with_prefix)
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


def get_main_file_name():
    files = [p.name for p in current_path.glob('*.py')]
    print('请选择烧录文件(如你想烧录的文件不在列表中，请将该文件复制到本目录下)：')
    for i in range(len(files)):
        print('[{}]: {}'.format(i, files[i]))
    i = input('请输入文件的序号(直接回车烧录框架)：')
    if not i:
        return None
    else:
        try:
            return files[int(i)]
        except Exception as e:
            print('输入错误！请关闭本窗口重试！')
            sys.exit()


if __name__ == '__main__':
    com = input('请输入COM端口号，可通过[WIN + X]快捷键，按[G]后，在设备管理器中查看，或者直接[回车]自动搜索： ')
    if not com:
        com = find_com()
        if not com:
            print('COM口没有找到！')
            sys.exit()
    if 'COM' not in com.upper():
        com = 'COM{}'.format(com)
    file = get_main_file_name()
    if flash(com, file):
        print('')
        print('')
        print('')
        print('↓↓↓↓↓↓↓↓↓↓请看下面提示！！！！↓↓↓↓↓↓↓↓↓↓↓')
        print('刷入成功！请按板子上的[RST]按钮或[CTRL + D]来运行！')
        print('刷入成功！请按板子上的[RST]按钮或[CTRL + D]来运行！')
        print('刷入成功！请按板子上的[RST]按钮或[CTRL + D]来运行！')
        print('刷入成功！请按板子上的[RST]按钮或[CTRL + D]来运行！')
        print('刷入成功！请按板子上的[RST]按钮或[CTRL + D]来运行！')
        print('刷入成功！请按板子上的[RST]按钮或[CTRL + D]来运行！')
        print('刷入成功！请按板子上的[RST]按钮或[CTRL + D]来运行！重要的事情说7遍都不为过！！！！！！')
        print('↑↑↑↑↑↑↑↑↑↑请看上面提示！！！！↑↑↑↑↑↑↑↑↑↑↑')
        print('')
        print('')
        print('')
        repl(com)
    else:
        print('刷入失败！请查看端口是否有被占用，可拔插后重试...')
        sys.exit()
