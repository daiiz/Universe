# -*- coding: utf-8 -*-
# Copyright 2015 daiz. All Rights Reserved.
# apricot version 0.0.4

import sys
import os
import datetime
import shutil
import re
import smtplib
import getpass
from email.mime.text import MIMEText

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

def build(basefile, outfile, rs, vs, rm, e):
    currentdir = os.getcwd()
    tmpfile = "apricot.tmp.{}".format(e)
    b = "{}/{}".format(currentdir, basefile)
    t = "{}/{}".format(currentdir, tmpfile)
    shutil.copy(b, t)
    # outputファイルを生成
    fl = open(outfile, 'w')

    # メイン処理
    f = open(tmpfile, 'r')
    codes = f.readlines()
    i = 0  # 行数
    #
    # 一行ずつ以下の処理を行う
    #
    for code in codes:
        #
        # remove codes の処理
        #
        i += 1
        for ptn in rm:
            ptn = ptn.split("=")[-1]
            if re.match(ptn, code) is not None:
                print "@{}:{} removed ({}): {}".format(tmpfile, i, ptn, code[:-1])
                code = ''
        #
        # set Values の処理
        #
        cmt = "{}set ".format(apricot_comment[e][0])  # ex. "/** apricot.set "
        pos = code.find(cmt)
        if pos >= 0:
            cmtb = " {}".format(apricot_comment[e][1])  # ex. " **/"
            vlabel = code.split(cmt)[-1].split(cmtb)[0]
            value = ''
            for v in vs:
                ptn = v.split("=")[0]
                if ptn == vlabel:
                    value = v.split("=")[-1]

            if value != '':
                rep = "{}set {} {}".format(apricot_comment[e][0], vlabel, apricot_comment[e][1])
                # ex. "/** apricot.set Va **/"
                code = code.replace(rep, value)
            print "@{}:{} setted ({}): {}".format(tmpfile, i, vlabel, value)
        #
        # import Resources の処理
        #
        cmt = "{}import ".format(apricot_comment[e][0])  # ex. "/** apricot.import "
        pos = code.find(cmt)
        if pos >= 0:
            cmtb = " {}".format(apricot_comment[e][1])  # ex. " **/"
            rstr = code.split(cmt)[-1].split(cmtb)[0]
            rfile = rstr.split("/")[0]
            rlabel = rstr.split("/")[-1]
            value = ''
            for r in rs:
                ptn = r.split("=")[0]
                if ptn == rlabel:
                    value = r.split("=")[-1]
            code_a = get_code(rfile, rlabel, value, e)
            rep = "{}import {}/{} {}".format(apricot_comment[e][0],
                                             rfile,
                                             rlabel,
                                             apricot_comment[e][1])
            if(code_a != ""):
                code = code.replace(rep, code_a)
                print "@{}:{} imported ({}/{}): {}".format(tmpfile, i, rfile, rlabel, value)
            else:
                code = "// {}".format(code)
                print "@{}:{} NOT imported ({}): {}".format(tmpfile, i, rlabel, value)
            #print code_a
        fl.write(code)
    f.close()
    fl.close()
    os.remove(tmpfile)
    return 1

def get_code(f, l, val, e):
    fl = file(f, 'r')
    content = fl.read()
    ptn = "{}R = ".format(apricot_comment[e][0])  # ex. "/** apricot.R = "
    snippets = content.split(ptn)
    q = "{} {}".format(val, apricot_comment[e][1])  # ex. "en **/"
    c = ""
    for snippet in snippets:
        pos = snippet.find(q)
        if pos == 0:
            cmt = apricot_comment[e][0].split(" ")[0]
            # c = "{} {}/{} = {}".format(cmt, f, l, snippet)
            c = snippet.split(q)[-1]
            # 改行コードを除去（win, mac, unix）
            c = c.lstrip();
            c = c.lstrip();
            fl.close()
            return c
    fl.close()
    return c
def gmail(toby, sub, txt):
    password = getpass.getpass()
    print "Sending... Please wait for a while."
    to = "{}@gmail.com".format(toby)
    by = "{}@gmail.com".format(toby)
    #txt = "This mail was sent by apricotPie."
    host, port = 'smtp.gmail.com', 465
    msg = MIMEText(txt)
    msg['Subject'] = sub
    msg['From'] = by
    msg['To'] = to

    smtp = smtplib.SMTP_SSL(host, port)
    smtp.ehlo()
    smtp.login(by, password)
    smtp.mail(by)
    smtp.rcpt(to)
    smtp.data(msg.as_string())
    smtp.quit()


def main():
    # コマンドラインを取得
    c = sys.argv
    if len(c) == 5:
        c.append(None)  # as remove_code

    # コマンドラインを解釈
    (apricot,
     task,
     output_file_name,
     build_options,
     encode,
     remove_code) = c

    # task
    mail = None
    mail_flag = 0
    if('-' in task):
        cmds = task.split("-")
        task = cmds[0]
        mail = cmds[1]
        print "Do you want to receive an e-mail to {}@gmai.com when the build is completed? (0 or 1)".format(mail)
        n = int(raw_input())
        if(n == 1):
            mail_flag = 1

    if task == "build":
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

        if(res == 1 and (mail is not None) and mail_flag == 1):
            # toby: USERNAME (NOT include "@gmail.com")
            toby = mail
            sub = "[apricotPie build-successful] {}".format(output_file_name)
            msg = "python {} {} {} {} {} {}".format(
                apricot,
                task,
                output_file_name,
                build_options,
                encode,
                remove_code)
            gmail(toby, sub, msg)
            res = "Mail sent."

        print res


if __name__ == '__main__':
    main()
