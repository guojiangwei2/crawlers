#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import logging
import cPickle
import pandas as pd
from collections import Counter

dir = 'data/'
f_lst = os.listdir(dir)
# crawled res with only inclued 2014-2016 infos
f_lst_2 = glob.glob('data/201[4-6]_*.pickle')


def rm_error_pickles():
    i = 0
    for fname in f_lst_2:
        with open(fname, 'r') as f:
            data = cPickle.load(f)
            if 'ErrorInfo' in data:
                os.remove(fname)
                i += 1
    print('remove error files {cnt}.'.format(cnt=i))


def select_data(json_dct, stknm, year):
    res = json_dct.get('Option', {}).get('ResultSection', {})
    if res:
        return pd.DataFrame.from_dict(res).assign(stknm=stknm).assign(year=year)
    else:
        logging.warn('{stknm} at {year} gets none data.'.format(stknm=stknm, year=year))
        return


def crawled_stats():
    res = [fname[:-7].split('_')[1] for fname in f_lst_2]
    c = Counter(res)
    crawled = [k for k, v in c.items() if v == 3]
    print('Congratulations, you have crawled {cnt} stks.'.format(cnt=len(crawled)))
    cPickle.dump(crawled, open('crawled_stks.pickle', 'w'))


def main():
    data_lst = [(f, cPickle.load(open(f, 'r'))) for f in f_lst_2]
    print('crawled data cnt is {cnt}.'.format(cnt=len(data_lst)))
    df_lst = [select_data(dct, fname[:-7].split('_')[1], fname[:-7].split('_')[0])\
              for (fname, dct) in data_lst]
    df_res = pd.concat(df_lst)\
        .loc[:, ('stknm', 'year', 'Database', 'Count')]\
        .set_index(['stknm', 'year', 'Database'])\
        .unstack()
    df_res.to_csv('stat_stk_innojoy_info.csv', sep='\t', encoding='utf-8')


if __name__ == '__main__':
    main()
    # crawled_stats() # 161 stocks
    # print(len(f_lst_2)) # 621
    # rm_error_pickles()
