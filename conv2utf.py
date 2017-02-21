import codecs
import os
import sys
import shutil
import re
import chardet
import chardet
import Dir

convertfiletypes = [
  ".cpp",
  ".h",
  ".hpp"
  ]

def get_filelist(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):
        fileList.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir=os.path.join(dir,s)
            get_filelist(newDir, fileList)
    return fileList

def convert_encoding(filename, target_encoding):
    # Backup the origin file.
    # convert file from the source encoding to target encoding
    try:
        content = codecs.open(filename,'r',encoding="GBK").read()
        codecs.open(filename, 'w', encoding=target_encoding).write(content)
    except Exception:
        print(filename)


def convert(dir):
    filelist =[]
    get_filelist(dir,filelist)
    print(dir)
    for filename in filelist:
        convert_encoding(filename, 'utf-8')

if __name__ == '__main__':
    # 典型案例111篇
    # 基础案例299篇-已标注
    dir  = Dir.resourceDir+"/已标注文书-txt/基础案例299篇-已标注/"
    convert(dir)