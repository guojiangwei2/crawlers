#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import cPickle
import requests
import pandas as pd

stknm_fname = 'stknm.xls'
stk_innojoy_res = 'stk_innojoy_info.csv'
url = 'http://www.innojoy.com/client/interface.aspx'

payload = {
    'patentSearchConfig': {
        'Action': 'Search',
        'AddOnes': '',
        'DBOnly': 0,
        'Database': 'fmsq,wgzl,syxx,fmzl',
        'DelOnes': '',
        'GUID': '',
        'Page': '1',
        'PageSize': '10',
        'Query': '',
        'RemoveOnes': '',
        'SmartSearch': '',
        'Sortby': '-IDX,PNM',
        'TreeQuery': '',
        'TrsField': '',
        'Verification': ''
    },
    'requestModule': 'PatentSearch',
    'userId': '587D23BB-3852-43A2-A44C-E606F22626E9'
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Content-Length': '366',
    'Content-Type': 'application/json',
    'Cookie': 'JSESSIONID=vb87dm46litr1at8rltyl0l5h; Hm_lvt_9ebd156ac7d2304301a6a7f0434e8257=1488609334; Hm_lpvt_9ebd156ac7d2304301a6a7f0434e8257=1488685121',
    'Host': 'www.innojoy.com',
    'Origin': 'http://www.innojoy.com',
    'Referer': 'http://www.innojoy.com/searchresult/default.html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}


def compose_payload(stknm, year):
    query_str = '{stknm} and ADY={year}'.format(stknm=stknm, year=year)
    payload['patentSearchConfig'].update({'Query': query_str})
    return json.dumps(payload)


def select_data(json_dct, stknm, year):
    cPickle.dump(json_dct, open('data/{year}_{stknm}.pickle'.format(year=year, stknm=stknm), 'w'))
    res = json_dct.get('Option', {}).get('ResultSection', {})
    return pd.DataFrame.from_dict(res).assign(stknm=stknm).assign(year=year)\
        if res else None


def cawl_by_stknm_year(stknm, year):
    payload = compose_payload(stknm=stknm, year=year)
    r = requests.post(url=url, data=payload, headers=headers)
    res = select_data(json_dct=r.json(), stknm=stknm, year=year)
    return res


def main():
    with open('crawled_stks.pickle', 'r') as f:
        crawled = cPickle.load(f)
    df_lst = []
    df_stk = pd.read_excel(stknm_fname, encoding='utf-8')
    # years = range(2010, 2017)
    years = range(2014, 2017)
    reverse_stknms = df_stk['Conme'].tolist()[::-1]
    i = 0
    # for stknm in df_stk['Conme']:
    for stknm in reverse_stknms:
    # for stknm in ['平安银行股份有限公司', '金田实业(集团)股份有限公司']:
        if stknm.encode('utf-8') in crawled:
            continue
        i += 1
        if i % 50 == 0:
            print('*')
        for year in years:
            df = cawl_by_stknm_year(stknm=stknm.encode('utf-8'), year=year)
            df_lst.append(df)
    cPickle.dump(df_lst, open('stk_innojoy_res.pickle', 'w'))
    df_res = pd.concat(df_lst)
    df_res.to_csv(stk_innojoy_res, sep='\t', encoding='utf-8')


if __name__ == '__main__':
    # payload = compose_payload('平安银行', 2014)
    # print(payload)
    # main()
    # year = 2014
    # conme = '平安银行'
    # res = cawl_by_stknm_year(stknm=conme, year=year)
    # print(res)
    main()
