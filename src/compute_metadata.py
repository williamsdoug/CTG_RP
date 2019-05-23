#!/usr/bin/env python
# coding: utf-8


import os
import json
from pprint import pprint
import random
import copy


def split_recordings_by_outcome(data, thresh, key='pH'):
    all_true = []
    all_false = []
    
    for k, v in data.items():
        if v['outcome'][key] >= thresh:
            all_true.append(k)
        else:
            all_false.append(k)
            
    random.shuffle(all_false)
    random.shuffle(all_true)
    
    n = min(len(all_false), len(all_true))
    all_false = all_false[:n]
    all_true = all_true[:n]
    
    return all_false, all_true


def compute_splits(all_false, all_true, n_splits=5):
    all_false, all_true = copy.copy(all_false), copy.copy(all_true)
    
    all_splits = []
    while n_splits > 0:
        if n_splits == 1:
            n = len(all_false)
        else:
            n = len(all_false) // n_splits
            
        all_splits.append({False: all_false[:n], True: all_true[:n]})
        all_false, all_true = all_false[n:], all_true[n:]
        n_splits -= 1
        
    random.shuffle(all_splits)   
    return all_splits


def assemble_splits(all_splits):
    groups = []
    for i in range(len(all_splits)):
        entry = {'train':{False: [], True: []}, 'valid':{False: [], True: []}}
        for j, d in enumerate(all_splits):
            key = 'valid' if i==j else 'train'
            for k, v in d.items():
                entry[key][k] += v
        groups.append(entry)
    return groups


def annotate_train_valid_group(group, data, exclude=[], include=[]):
    results = {'train':{False: [], True: []}, 'valid':{False: [], True: []}}
    for k, v in group.items():
        for kk, vv in v.items():
            for recno in vv:
                for fname in data[recno]['names']:
                    ignore = False
                    for txt in exclude:
                        if txt in fname:
                            ignore = True
                    if ignore:
                        continue
                        
                    if include:
                        for txt in include:
                            if txt in fname:
                                results[k][kk].append(fname)
                                break
                    else:
                        results[k][kk].append(fname)

    return results  



def get_splits(image_dir='images', image_file='rp_images_index.json', 
               thresh = 7.15, exclude=[], include=[], verbose=False):
    random.seed(1234)
    with open(os.path.join(image_dir, image_file), 'r') as infile:
            data = json.load(infile)  

    all_false, all_true = split_recordings_by_outcome(data, thresh, key='pH')
    all_selected = all_false + all_true
    all_splits = compute_splits(all_false, all_true, n_splits=5)
    
    train_valid_groups = assemble_splits(all_splits)
    if verbose:
        for v in train_valid_groups:
            print('train', len(v['train'][True]), len(v['train'][False]))
            print('valid', len(v['valid'][True]), len(v['valid'][False]))
            print('')
    
    train_valid_groups_full = []
    for v in train_valid_groups:
        train_valid_groups_full.append(
            annotate_train_valid_group(v, data, exclude=exclude, include=include))
        
    return train_valid_groups_full


def generate_label_file(group, image_dir='images', 
                        csv_file='labels.csv', header='fname, label'):
    if csv_file is None:
        results = []
        for v in group.values():
            for label, all_files in v.items():
                for fname in all_files:
                    results.append((os.path.join(image_dir, fname), 1 if label else 0))
        return results
    else:
        with open(os.path.join(image_dir, csv_file), 'wt') as outfile:
            if header:
                print(header, file=outfile)
            for v in group.values():
                for label, all_files in v.items():
                    for fname in all_files:
                        line = '{}, {}'.format(fname, 1 if label else 0)
                        print(line, file=outfile)


def OLDgenerate_lists(group, image_dir='images', train_file='train.csv',
                        valid_file='valid.csv', header='fname, label'):
    for k, csv_file in [['train', train_file], ['valid',valid_file ]]:
        with open(csv_file, 'wt') as outfile:
            if header:
                print(header, file=outfile)
            for label, all_files in group[k].items():
                for fname in all_files:
                        line = '{}, {}'.format(os.path.join(image_dir, fname), 1 if label else 0)
                        print(line, file=outfile)



def generate_lists(group, image_dir='images', train_file='train.csv',
                        valid_file='valid.csv', header='fname, label'):
    for k, csv_file in [['train', train_file], ['valid',valid_file ]]:
        with open(os.path.join(image_dir, csv_file), 'wt') as outfile:
            if header:
                print(header, file=outfile)
            for label, all_files in group[k].items():
                for fname in all_files:
                        line = '{}, {}'.format(fname, 1 if label else 0)
                        print(line, file=outfile)




