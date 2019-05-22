GITHUB_PREFIX = 'https://raw.githubusercontent.com/williamsdoug/CTG_RP/master/src/'
GITHUB_DEFAULT_SRC_FILES = ['test.py']

def get_github_files(flist):
    import urllib.request
    import os

    for fname in flist:
        try:
            if '*' not in fname and '/' not in fname and '?' not in fname:
                print('Beginning file download of file', fname)
                print(GITHUB_PREFIX+fname)
                try:
                    os.remove(fname)
                except:
                    pass
                urllib.request.urlretrieve(GITHUB_PREFIX+fname, fname)
            else:
                print('Skipping file download of file', fname)
        except:
            print('Download failed for file', fname)
    print('Done')

def get_default_github_src_files():
    get_github_files(GITHUB_DEFAULT_SRC_FILES)