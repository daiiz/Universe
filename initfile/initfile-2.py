## initfile-2.py
## Generated in 2015-01-10 00:13:28.

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