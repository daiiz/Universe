## publish-1.py
## Generated in 2015-01-10 00:37:38.

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