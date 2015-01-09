## get_project_name-1.py
## Generated in 2015-01-09 23:26:47.

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