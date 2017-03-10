#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd

stknm_fname = 'stknm.xls'
stknm_wind_fname = 'stkcd_briefnm_location.xlsx'
stknm_chg_hist_fname = 'stknm_hist.xlsx'
stknm_merged_txt = 'stknm_merged.txt'


def main():
    df_old = pd.read_excel(stknm_fname, encoding='utf-8')
    df_wind = pd.read_excel(stknm_wind_fname, encoding='utf-8')
    df_chg = pd.read_excel(stknm_chg_hist_fname, encoding='utf-8')
    stk_lst = []
    stk_lst.extend(df_old.iloc[:, 2].dropna().tolist())
    stk_lst.extend(df_wind.iloc[:, 2].dropna().tolist())
    stk_lst.extend(df_chg.iloc[:, 2].dropna().tolist())
    stk_lst.extend(df_chg.iloc[:, 3].dropna().tolist())
    print('Total stknm is {cnt}.'.format(cnt=len(set(stk_lst))))
    # UGLY try encode and decode
    # with codecs.open(stknm_merged_lst, 'wb', encoding='utf-8') as f:
    with open(stknm_merged_txt, 'w') as f:
        stk_set = set([stk.encode('utf-8') for stk in stk_lst])
        f.write(','.join(list(stk_set)))


def print_res():
    with open(stknm_merged_txt, 'r') as f:
        line = f.read()
    with open('stknm_merged_2.txt', 'w') as f:
        lines = line.replace(',', '\n')
        f.write(lines)


if __name__ == '__main__':
    # main()
    print_res()
