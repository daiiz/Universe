## get_timestamp-1.py
## Generated in 2015-01-09 23:26:30.

def get_timestamp():
    now = datetime.datetime.now()
    #now.strftime("%Y/%m/%d %H:%M:%S")
    return "{0:%Y-%m-%d %H:%M:%S}".format(now)