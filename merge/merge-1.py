## merge-1.py
## Generated in 2015-01-09 23:27:24.

def merge(paths, outfile, copyright, comment_head):
    # マージしたファイル数
    num = 0
    # 出力ファイルが既存の場合はpre化する
    if(os.path.exists(outfile) is True):
        os.rename(outfile, outfile+'.pre')
    # 出力ファイルを生成する
    out_f = open(outfile, 'w')
    out_f.write(comment_head + outfile + '\n')
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