def test():
    print('Low There')

def get_github_files(flist, prefix = 'https://raw.githubusercontent.com/williamsdoug/CTG_RP/master/src/'):
    import urllib.request
    import os

    for fname in flist:
        try:
            print('Beginning file download of file', fname)
            os.remove(fname)
            urllib.request.urlretrieve(prefix+fname, fname)
        except:
            print('Download failed for file', fname)
    print('Done')
