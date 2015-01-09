## nobr-1.py
## Generated in 2015-01-09 23:27:08.

def nobr(str):
    # 文字列の末尾から改行コードを取り除く
    if(str[-1] == '\n'): str = str[:-1]
    if(str[-1] == '\r'): str = str[:-1] 
    return str