
logfile_path = 'log.txt'# = open('log.txt', 'a')
def log(s: str):
    with open(logfile_path, 'a') as logfile:
        s = ''.join([c for c in s if c.isascii()])
        print(s, end="\n", file=logfile)
