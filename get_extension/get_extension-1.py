## get_extension-1.py
## Generated in 2015-01-09 23:26:38.

def get_extension(file_name):
    # file_name: 拡張子付きのファイル名
    names = file_name.split(".")
    extension = names[-1]
    return extension