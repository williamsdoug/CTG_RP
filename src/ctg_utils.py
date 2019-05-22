import wfdb
import os
from pprint import pprint

import numpy as np
import matplotlib.pyplot as plt
import scipy
import scipy.signal

def get_all_recno(dbdir):
    for f in os.listdir(dbdir) :
        if os.path.isfile(os.path.join(dbdir, f)) and f.endswith('.hea'):
            yield f.split('.')[0]
            

def parse_meta_comments(comments, verbose=False):
    result = {}
    for c in comments:
        # print(c)
        if c.startswith('---'):
            continue
        if c.startswith('-- '):
            entry = {}
            k = c.split()[1]
            result[k] = entry
            continue
        c = c.strip()
        idx = c.rfind(' ')
        k = c[:idx].strip()
        v = c[idx+1:]
        
        try:
            v = int(v)
        except Exception:
            try:
                v = float(v)
            except Exception:
                pass
        entry[k] = v
        if verbose:
            print('  {}:{} ({})'.format(k, v, type(v)))
    return result


def physionet_ctg_generate_mask(sig):
    mask = (sig != 0)
    all_idx = np.arange(len(sig))
    
    new_sig = np.interp(all_idx, all_idx[mask], sig[mask])
    return mask, new_sig
