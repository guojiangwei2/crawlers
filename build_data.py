# -*- coding: utf-8 -*-

import pandas as pd
from consts import raw_csv, candi_csv


def build_data():
    df_raw = pd.read_csv(raw_csv, encoding='utf-8')
    res = []
    for _, row in df_raw.fillna('').iterrows():
        stkcd = row['stkcd']
        year = row['year']
        stock = row['stock']
        name = row['name']
        if not name:
            if stock:
                name = stock
            else:
                print(stock, name)
        if year == 2016:
            res.append((stkcd, stock, name, 2015))
        else:
            for i in (-1, 0, 1):
                _year = year + i
                res.append((stkcd, stock, name, _year))
    df_res = pd.DataFrame(list(set(res)), columns=['stkcd', 'stock', 'name', 'year']) \
        .assign(is_crawled=0) \
        .sort_values(by=['stkcd', 'stock', 'year'])
    df_res.to_csv(candi_csv, encoding='utf-8', index=False)


def merge_is_crawled():
    df_labeled = pd.read_csv('data/candi_bak.csv', encoding='utf-8', dtype={'stkcd': str})
    df_candi = pd.read_csv('data/candi.csv', encoding='utf-8', dtype={'stkcd': str})
    df_res = df_candi \
        .drop(labels=['is_crawled'], axis=1) \
        .merge(df_labeled, on=['stkcd', 'stock', 'year', 'name'], how='left') \
        .fillna(0)
    df_res.to_csv('data/candi.csv', encoding='utf-8', index=False)


if __name__ == "__main__":
    # build_data()
    merge_is_crawled()
