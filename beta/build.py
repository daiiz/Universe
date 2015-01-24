#** apricot.R = 1 **#
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