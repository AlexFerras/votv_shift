import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--run', action='store_true')
parser.add_argument('-f', '--force', action='store_true')


args = parser.parse_args()

ACTUAL_LINK = 'https://www.dropbox.com/scl/fi/mx8nsvgpd8g0r71zz1lwm/votv_shift.zip?rlkey=evpucmigpcv3cggi2xim3elov&st=jcmptqe3&dl=1'
if not args.force:
    import cgi
    import urllib
    import urllib.request
    
    response = urllib.request.urlopen(ACTUAL_LINK)
    _, params = cgi.parse_header(response.headers.get('Content-Disposition', ''))
    filename = params['filename']
    import re
    PATTERN = r'\d+.\d+.\d+'
    NEW_VERSION = tuple([int(i) for i in re.search(PATTERN, filename).group(0).split('.')])


    with open('version.txt') as f:
        l = f.readline()
        CURRENT_VERSION:tuple = ()
        CURRENT_VERSION = tuple([int(i) for i in l.split('.')])

    if NEW_VERSION == CURRENT_VERSION:
        print('updating')
    else:
        exit()
import urllib.request

try:
    response = urllib.request.urlopen(ACTUAL_LINK)
    _, params = cgi.parse_header(response.headers.get('Content-Disposition', ''))
    filename = params['filename']
    import re
    PATTERN = r'\d+.\d+.\d+'
    NEW_VERSION = tuple([int(i) for i in re.search(PATTERN, filename).group(0).split('.')])
    print(NEW_VERSION)
except:
    filename = 'newversion.zip'

urllib.request.urlretrieve(ACTUAL_LINK, filename)
from zipfile import ZipFile
with ZipFile(filename) as zf:
    top_dir = zf.namelist()
    for e in zf.namelist(): 
        if e == 'updater.exe':
            continue
    zf.extract(e)
    try:
        os.rename('updater.exe', 'updater.bak')
    except:
        pass
    zf.extract('updater.exe')

