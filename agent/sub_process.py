# -*- coding: utf-8 -*-
"""
Created on Tue May  8 14:45:26 2018

@author: MERLIN.MA
"""
def install(spath):
    import subprocess,os
    p, f = os.path.split(spath)
    print(p)
    print(f)
    os.chdir(p)
    subprocess.call(f)