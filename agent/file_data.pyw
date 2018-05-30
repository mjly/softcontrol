#! python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 10 09:45:00 2018

@author: MERLIN.MA
"""

import hashlib
import os
import pythoncom
import win32ui
from win32com.shell import shell

def get_file_name():
    dlg = win32ui.CreateFileDialog(1)  # 1表示打开文件对话框

    dlg.SetOFNInitialDir('D:/')  # 设置打开文件对话框中的初始显示目录

    dlg.DoModal()

    filename = dlg.GetPathName()  # 获取选择的文件名称
    #print(filename)
    return filename

def GetpathFromLink(lnkpath):
    shortcut = pythoncom.CoCreateInstance(
        shell.CLSID_ShellLink, None,
        pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink)
    shortcut.QueryInterface(pythoncom.IID_IPersistFile).Load(lnkpath)
    path = shortcut.GetPath(shell.SLGP_SHORTPATH)[0]
    return path


def CalcSha1(filepath):
    with open(filepath, 'rb') as f:
        sha1obj = hashlib.sha1()
        sha1obj.update(f.read())
        hash = sha1obj.hexdigest()
        #print(hash)
        return hash


def CalcMD5(filepath):
    with open(filepath, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        hash = md5obj.hexdigest()
       # print(hash)
        return hash


def getData():
    file_name = get_file_name()
    hashfile = None
    if file_name.endswith('.lnk'):
        hashfile = GetpathFromLink(file_name)
    else:
        hashfile = file_name

    if not os.path.exists(hashfile):

        hashfile = os.path.join(os.path.dirname(__file__), hashfile)
        if not os.path.exists(hashfile):
            return ("cannot found file",' ',' ')
        else:
            file_md5 = CalcMD5(hashfile)
            file_sha1 = CalcSha1(hashfile)
            return (hashfile + ' ' + file_md5 + ' ' + file_sha1)
    else:
        file_md5 = CalcMD5(hashfile)
        file_sha1 = CalcSha1(hashfile)
        return (hashfile,file_md5,file_sha1)

        # raw_input("pause")

