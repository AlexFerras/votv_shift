import os

with open(os.path.join(os.getcwd(), 'votv_shift.py')) as f:
    l = f.readline()
    VERSION:tuple = ()
    exec(l, globals())
    fv = VERSION + (0,)

with open(os.path.join(os.getcwd(), 'version_file.txt')) as f:
    lines = f.readlines()
    lines[2] = f'    filevers={str(fv)},\n'
    print(lines[2])
with open(os.path.join(os.getcwd(), 'version_file.txt'), 'w') as f:
    f.writelines(lines)


with open(os.path.join(os.getcwd(), 'version.txt'), 'w') as f:
    f.write('.'.join([str(s) for s in VERSION]))
