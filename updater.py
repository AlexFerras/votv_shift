import os
import argparse

import urllib.request
import cgi
parser = argparse.ArgumentParser()
parser.add_argument('-r', '--run', action='store_true')
parser.add_argument('-f', '--force', action='store_true')
parser.add_argument('-l', '--local', action='store_true')

FORCE = False



args = parser.parse_args()
import re
PATTERN = r'\d+.\d+.\d+'

if args.local:
    USE_LOCAL_ARCHIVE = "E:\\Projects\\VoicesOfTheVoid\\PythonUI\\votv_shift.zip"

try:

    if not args.force and not FORCE:
        import cgi
        import urllib
        import urllib.request
        
        verline = urllib.request.urlopen('https://alexferras.github.io/votv.txt').read()
        NEW_VERSION = tuple([int(i) for i in verline.decode().split('.')])


        with open('version.txt') as f:
            l = f.readline()
            CURRENT_VERSION:tuple = ()
            CURRENT_VERSION = tuple([int(i) for i in l.split('.')])

        if NEW_VERSION > CURRENT_VERSION:
            print('updating')
        else:
            print('no need for update')
            import sys
            sys.exit()
    print('updating votv shift')
    try:
        USE_LOCAL_ARCHIVE
        import shutil
        shutil.copy2(USE_LOCAL_ARCHIVE, os.getcwd())
        filename = os.path.basename(USE_LOCAL_ARCHIVE)
    except:
        ACTUAL_LINK = 'https://www.dropbox.com/scl/fi/mx8nsvgpd8g0r71zz1lwm/votv_shift.zip?rlkey=evpucmigpcv3cggi2xim3elov&st=jcmptqe3&dl=1'
        response = urllib.request.urlopen(ACTUAL_LINK)
        _, params = cgi.parse_header(response.headers.get('Content-Disposition', ''))
        filename = params['filename']
        urllib.request.urlretrieve(ACTUAL_LINK, filename)
    from zipfile import ZipFile
    # extracting archive
    with ZipFile(filename) as zf:
        for e in zf.infolist():
            e.filename = e.filename.removeprefix('votv_shift/')
            if e.filename.endswith('/'):
                continue

            if e.filename == 'updater.exe':
                if os.path.exists('updater.bak'):
                    os.remove('updater.bak')
                e.filename = 'updater.bak'
                zf.extract(e)
                continue

            if e.filename:
                if os.path.exists(e.filename):
                    os.remove(e.filename)
                zf.extract(e)
            

    

    #os.remove('updater.bak')
    os.remove(filename)
    if args.run:
        os.system('start votv_shift')
except Exception as e:
    print(e)
    input('error')