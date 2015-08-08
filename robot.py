# -*- coding:utf-8 -*-

import os
import glob


os.chdir('downloads/gitbooks')
for x in glob.glob('*'):
    if os.path.isdir(x):
        flag = False
        for root, dirs, _ in os.walk(x):
            for d in dirs:
                if d == 'gitbook':
                    os.system('cp -rf ../../assets/fonts %s' %
                              os.path.join(root, d))
                    flag = True
                    break
            if flag:
                break
        os.system('zip -r %s %s' % ('../zips/' + x + '.zip', x, ))
