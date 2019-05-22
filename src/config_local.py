def test():
    print('Low There')

def get_github_files(flist, prefix = 'https://raw.githubusercontent.com/williamsdoug/CTG_RP/master/src/'):
    import urllib.request

    for fname in flist:
        print('Beginning file download of file', fname)
        urllib.request.urlretrieve(prefix+fname, fname)