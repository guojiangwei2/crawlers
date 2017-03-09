#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import json
import cPickle
import logging
import requests
import commands

url = 'http://www.innojoy.com/client/interface.aspx'
data_dir = 'data/'
crawled_file_lst = os.listdir(data_dir)
stknm_merged_txt = 'stknm_merged.txt'
stknm_crawled_txt = 'crawled_stknms.txt'

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
    query_str = '\'{stknm}\' and ADY={year}'.format(stknm=stknm, year=year)
    payload['patentSearchConfig'].update({'Query': query_str})
    return json.dumps(payload)


def select_data(json_dct, stknm, year):
    cPickle.dump(json_dct, open('data/{year}_{stknm}.pickle'.format(year=year, stknm=stknm), 'w'))
    # res = json_dct.get('Option', {}).get('ResultSection', {})


def crawl_by_stknm_year(stknm, year):
    time.sleep(2)
    payload = compose_payload(stknm=stknm, year=year)
    r = requests.post(url=url, data=payload, headers=headers)
    if 'ErrorInfo' in r.json():
        logging.warn('ERRORS: {stknm}_{year} encounter {error}.'\
                     .format(stknm=stknm,
                             year=year,
                             error=r.json()['ErrorInfo'].encode('utf-8')
                             )
                     )
    else:
        # just save crawled data, not select immediately
        select_data(json_dct=r.json(), stknm=stknm, year=year)


def main():
    with open(stknm_merged_txt, 'r') as f:
        stknm_lst = f.read().split(',')
    i, years = 0, range(2014, 2017)
    for stknm in stknm_lst:
        for year in years:
            if '{year}_{stknm}.pickle'.format(year=year, stknm=stknm) \
                    in crawled_file_lst:
                continue
            crawl_by_stknm_year(stknm=stknm, year=year)
        commands.getstatusoutput("echo {stknm} >> {fname}".\
                                 format(stknm=stknm, fname=stknm_crawled_txt))
        i += 1
        if i % 100 == 0:
            logging.info('You have crawled {pct}% stks.'.format(pct='%0f' % (i * 100.0 / 3700)))


if __name__ == '__main__':
    main()
