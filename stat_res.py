#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import logging
import cPickle
import pandas as pd

target_flst = glob.glob('data/201*.pickle')
res_csv = 'crawled_stat.csv'


def select_data(resp_json, stknm, year):
    try:
        res = resp_json.get('Option', {}).get('ResultSection', {})
        if res:
            return pd.DataFrame.from_dict(res).assign(stknm=stknm).assign(year=year)
        else:
            logging.warn('{stknm} at {year} gets none data.'.format(stknm=stknm, year=year))
            return
    except Exception as e:
        print(repr(e))


def main():
    data_lst = [(f, cPickle.load(open(f, 'r'))) for f in target_flst]
    # print('crawled data cnt is {cnt}.'.format(cnt=len(data_lst)))
    df_lst = [select_data(dct, fname[:-7].split('_')[1], fname[:-7].split('_')[0])
              for (fname, dct) in data_lst]
    df_res = pd.concat(df_lst).loc[:, ('stknm', 'year', 'Database', 'Count')] \
        .set_index(['stknm', 'year', 'Database']) \
        .unstack() \
        .reset_index()
    df_res.to_csv(res_csv, sep='\t', encoding='utf-8')


if __name__ == '__main__':
    main()
