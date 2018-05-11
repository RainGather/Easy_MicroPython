import os
import sys
import pathlib
import subprocess


try:
    from mp import mpfshell
except Exception as e:
    print('未找到所需库文件mpfshell, 尝试自动安装中...')
    subprocess.check_call('pip install mpfshell -i https://pypi.douban.com/simple')
    print('安装完成，请关闭本窗口重试。')
    sys.exit()
    

# current_dir = os.path.split(os.path.realpath(__file__))[0]
current_path = pathlib.Path('.')
os.chdir(current_path)


def flash(com, file):
    add_prefix(file)
    print('刷入中，请等待，请不要断开连接，或断电，或对板子做任何操作，包括拔插线头，如长时间未反应，请直接关闭本窗口重试...')
    cmd = 'python -m mp.mpfshell --open {} -n -c \"lcd cache;put main.py\"'.format(com)
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
        if 'from ezmpy import ' not in main_with_prefix:
            main_with_prefix = 'from ezmpy import *\n' + main_with_prefix
        if '@' in main_with_prefix and '\nrun()' not in main_with_prefix:
            main_with_prefix += '\nrun()\n'
    with (current_path / 'cache' / 'main.py').open('w', encoding='utf-8') as fw:
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
    files = [p.name for p in current_path.glob('*.py') if p.name.lower() not in ['flash.py', 'upload.py', 'build.py']]
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
    if len(sys.argv) <= 1:
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
        else:
            print('刷入失败！请查看端口是否有被占用，可拔插后重试...')
            sys.exit()
    repl(com)
