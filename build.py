import pathlib
import subprocess


p = pathlib.Path('.')

subprocess.call('rm ezmpy/* -rf', shell=True)

for i in list(p.glob('src/*.py')):
    subprocess.call('./mpy-cross {}'.format(i), shell=True)

subprocess.call('mv src/*.mpy ezmpy/', shell=True)
    
print('done')

