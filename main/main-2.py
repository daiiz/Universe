## main-2.py
## Generated in 2015-01-10 00:52:05.
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