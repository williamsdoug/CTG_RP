#
# Colab Notebook Configuration
#


GITHUB_PREFIX = 'https://raw.githubusercontent.com/williamsdoug/CTG_RP/master/src/'
GITHUB_DEFAULT_SRC_FILES = [
    'basic_denoise.py',
    'compute_metadata.py',
    'ctg_utils.py',
    'libRP.py',
    'test.py',  # used for test purposes only, TODO:  Delete after development complete
    ]

RECORDINGS_DIR = '/content/ctu-uhb-ctgdb'
IMAGES_DIR = '/content/images'


def try_remove_python_file(fname):
    from pathlib import Path
    try:
        import_file = Path() / fname
        import_file.unlink()
    except:
        pass


def try_remove_python_file_old(fname):
    import os
    try:
        os.remove(fname)
    except:
        pass


def get_github_files(flist):
    import urllib.request

    for fname in flist:
        try:
            if '*' not in fname and '/' not in fname and '?' not in fname:
                print('Beginning file download of file', fname)
                print(GITHUB_PREFIX+fname)

                try_remove_python_file(fname)
                urllib.request.urlretrieve(GITHUB_PREFIX+fname, fname)
            else:
                print('Skipping file download of file', fname)
        except:
            print('Download failed for file', fname)
    print('Done')


def get_default_github_src_files():
    get_github_files(GITHUB_DEFAULT_SRC_FILES)