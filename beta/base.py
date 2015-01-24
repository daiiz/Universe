# -*- coding: utf-8 -*-
# Copyright 2015 daiz. All Rights Reserved.
# apricot version #** apricot.set Vv **#

import sys
import os
import datetime
import shutil
import re

apricot_comment = {
    "js":  ["/** apricot.", "**/"],
    "c":   ["/** apricot.", "**/"],
    "py":  ["#** apricot.", "**#"],
    "h" :  ["/** apricot.", "**/"],
    "asm": ["#** apricot.", "**#"]
}

def printd(data):
    '''配列データをカンマ区切りで表示する'''
    print ("{}".format(data))[1:-1]

#** apricot.import build.py/R_build **#

def main():
    # コマンドラインを取得
    c = sys.argv
    if len(c) == 5:
        c.append(None)

    # コマンドラインを解釈
    (apricot, 
     task, 
     output_file_name, 
     build_options, 
     encode, 
     remove_code) = c

    # ビルドオプションを解釈
    options = build_options.split(",")
    base_file_name = options[0]
    R = []
    V = []
    for opt in options:
        if opt != base_file_name :
            if opt[0] == 'R':
                R.append(opt)
            elif opt[0] == 'V':
                V.append(opt)
    
    # ベースファイルの拡張子を取得
    extension = base_file_name.split(".")[-1]
    
    # ビルド時に取り除くコードのヘッド条件を保持
    rm = []
    if remove_code is not None:
        rm = remove_code.split(",")

    # ビルドコール
    res = build(base_file_name,
                output_file_name,
                R,
                V,
                rm,
                extension)  # 1ならば成功

    print res

if __name__ == '__main__':
    main()