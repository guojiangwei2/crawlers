#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import cPickle
import pandas as pd
from collections import Counter

dir = 'data/'
f_lst = os.listdir(dir)
f_lst_2 = glob.glob('201[4-6]_*.pickle')


def select_data(json_dct, stknm, year):
    cPickle.dump(json_dct, open('data/{year}_{stknm}.pickle'.format(year=year, stknm=stknm), 'w'))
    res = json_dct.get('Option', {}).get('ResultSection', {})
    return pd.DataFrame.from_dict(res).assign(stknm=stknm).assign(year=year)\
        if res else None


def crawled_stats():
    # download 182 stks the first days
    res = [fname[:-7].split('_')[1] for fname in f_lst]
    c = Counter(res)
    crawled = [k for k, v in c.items() if v == 7]
    cPickle.dump(crawled, open('crawled_stks.pickle', 'w'))


def main():
    data_lst = [(f, cPickle.load(open('data/{fname}'.format(fname=f), 'r'))) for f in f_lst]
    df_lst = [select_data(dct, fname[:-7].split('_')[1], fname[:-7].split('_')[0])\
              for (fname, dct) in data_lst]
    df_res = pd.concat(df_lst)\
        .loc[:, ('stknm', 'year', 'Database', 'Count')]\
        .set_index(['stknm', 'year', 'Database'])\
        .unstack()
    df_res.to_csv('stat_stk_innojoy_info.csv', sep='\t', encoding='utf-8')


if __name__ == '__main__':
    main()
    # crawled_stats()
    # f_lst_2 = glob.glob('data/201[4-6]_*.pickle')
    # print(len(f_lst_2))
    # 3108