## mkdir-1.py
## Generated in 2015-01-09 23:27:01.

def mkdir(relative_path):
    # カウントディレクトリにフォルダを作る
    if(os.path.exists(relative_path) is False):
        os.mkdir(relative_path)
        print "Initialized '/"+ relative_path +"'."