import pathlib
import subprocess


p = pathlib.Path('.')

subprocess.call('rm ./framework/ezmpy/*.mpy -rf', shell=True)

for i in list(p.glob('./src/*.py')):
    subprocess.call('./mpy-cross {}'.format(i), shell=True)

subprocess.call('mv ./src/*.mpy ./framework/ezmpy/', shell=True)
    
print('done')
