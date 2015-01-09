# -*- coding: utf-8 -*-

import sys
import os
import datetime

apricot_comment_style = {
    "js": "//// ",
    "c": "//// ",
    "py": "## ",
    "h": "//// ",
    "default": "//// "
}


def get_timestamp():
    now = datetime.datetime.now()
    #now.strftime("%Y/%m/%d %H:%M:%S")
    return "{0:%Y-%m-%d %H:%M:%S}".format(now)


def get_extension(file_name):
    # file_name: 拡張子付きのファイル名
    names = file_name.split(".")
    extension = names[-1]
    return extension


def get_project_name(file_name):
    # file_name: 拡張子付きのファイル名
    # project_name: 拡張子なしのファイル名
    names = file_name.split(".")
    project_name = ''
    for i in range(0, len(names)-1):
        # 拡張子以外のドットをハイフンに置換する
        project_name += names[i] + '-'
    project_name = project_name[:-1]
    return project_name


def mkdir(relative_path):
    # カウントディレクトリにフォルダを作る
    if(os.path.exists(relative_path) is False):
        os.mkdir(relative_path)
        print "Initialized '/"+ relative_path +"'."


def nobr(str):
    # 文字列の末尾から改行コードを取り除く
    if(str[-1] == '\n'): str = str[:-1]
    if(str[-1] == '\r'): str = str[:-1] 
    return str


def initfile(project_name, extension, comment_head):
    # 最新のバージョンナンバーを取得する
    files = os.listdir(project_name)
    version = 0
    # 既存の最新バージョン
    maxed_version = 0
    for fl in files:
        names = fl.split('.')
        # 拡張子が一致するファイルにのみ実行する
        if(names[-1] == extension):
            # ハイフン区切りの最後の要素がバージョンである
            version = (names[0].split('-'))[-1]
            if(int(version) > int(maxed_version)):
                maxed_version = version
    version = int(maxed_version) + 1
    fl_name = "{}-{}.{}".format(project_name, version, extension)
    # 現在の日時を取得する
    now = get_timestamp()
    newfile = open(project_name+'/'+fl_name, "w")
    newfile.write(comment_head + fl_name + '\n')
    newfile.write(comment_head + "Generated in "+ str(now) +".")
    newfile.close()
    print "Created '{}/{}'.".format(project_name, fl_name)


def publish(maerged_file_path, comment_head):
    # マージされたファイルから、apricotコメントヘッダを除去する
    # 公開・提出時などに、細分ファイルの生成日付情報などを取り除くために呼ばれる
    # 出力ファイル名前にプリフィックス「pub」を付加する
    prefix = "pub."
    if(os.path.exists(maerged_file_path) is True):
        fl = open(maerged_file_path, 'r')
        contents = fl.readlines()
        pub_fl = open(prefix+maerged_file_path, 'w')
        
        for code in contents:
            # 先頭からapricotコメントヘッダを探索する
            # 結果が0でない場合、pubに書き込む
            pos = code.find(comment_head)
            if(pos is not 0): 
                pub_fl.write(code)
        pub_fl.close()

        fl.close()
    print "Published '{}'.".format(prefix+maerged_file_path)


def merge(paths, outfile, copyright, comment_head, edition):
    # マージしたファイル数
    num = 0
    # 出力ファイルが既存の場合はpre化する
    if(os.path.exists(outfile) is True):
        os.rename(outfile, outfile+'.pre')
    # 出力ファイルを生成する
    out_f = open(outfile, 'w')
    # 通常のコメントヘッダ形式にする
    normal_comment_head = comment_head[0:len(comment_head)/2]
    out_f.write(normal_comment_head + " -*- coding: utf-8 -*-\n")
    out_f.write(comment_head + outfile + ' (' + edition + '-build)\n')
    out_f.write(comment_head + copyright + '\n')
    print "Merging...\n"
    for path in paths:
        if(os.path.exists(path) is True):
            in_f = file(path, 'r')
            content = in_f.read()
            out_f.write(content + '\n\n')
            num += 1
            print "> {}".format(path)
    in_f.close()
    out_f.close()
    print "------"
    print "Merged {} files as {}.".format(num, outfile)

def main():
    argvs = sys.argv
    # 引数からコマンド情報を取得する
    if(len(argvs) > 0):
        command = argvs[1]
        
        # 初期化コマンドの場合
        if(command == "init"):
            # プロジェクト名（拡張子のないファイル名）と拡張子を取得する
            dir_name = get_project_name(argvs[2])
            extension = get_extension(argvs[2])
            # プロジェクトフォルダを作る
            mkdir(dir_name)
            # プロジェクトファイルを作成し初期化する
            #TODO: comment head関数化
            comment = apricot_comment_style["default"]
            if(extension in apricot_comment_style):
                comment = apricot_comment_style[extension]
            initfile(dir_name, extension, comment)

        # マージコマンドまたは公開コマンドの場合
        elif(command == "merge" or command == "publish"):
            # リリースファイルを読む
            # 出力ファイル名とその拡張子を取得する
            file = open(argvs[2], "r")
            txts = file.readlines()
            output_file_name = nobr(txts[0])
            extension = nobr(output_file_name.split('.')[-1])
            # 著作者名を取得し、コピーライトを生成する
            author = nobr(txts[1])
            #TODO: get year
            year = "2015"
            copyright = 'Copyright {} {}. All Rights Reserved.\n'.format(year, author)
            # マージするファイルのパスを収集する
            paths = []
            for i in range(3, len(txts)):
                fl = txts[i]
                project = nobr(fl.split(' ')[0])
                version = nobr(fl.split(' ')[-1])
                path = '{}/{}-{}.{}'.format(project, project, version, extension)
                paths.append(path)
            file.close()
            comment = apricot_comment_style["default"]
            if(extension in apricot_comment_style):
                comment = apricot_comment_style[extension]
            merge(paths, output_file_name, copyright, comment, argvs[2])
            
            # 公開コマンドの場合のみ実行する
            if(command == "publish"):
                publish(output_file_name, comment)
        else:
            print ''
    print ''
print ''


if __name__ == '__main__':
    main()

