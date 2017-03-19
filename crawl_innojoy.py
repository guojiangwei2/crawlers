#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
import time
import cPickle
import logging
import requests
import commands
from consts import payload, headers, target_stknms_txt, crawled_stknms_txt

url = 'http://www.innojoy.com/client/interface.aspx'


def compose_payload(stknm, year):
    query_str = '\'{stknm}\' and ADY={year}'.format(stknm=stknm, year=year)
    payload['patentSearchConfig'].update({'Query': query_str})
    return json.dumps(payload)


def dump_data(json_dct, stknm, year):
    cPickle.dump(json_dct, open('data/{year}_{stknm}.pickle'.format(year=year, stknm=stknm), 'w'))


def crawl_by_stknm_year(stknm, year):
    payload = compose_payload(stknm=stknm, year=year)
    # use while to solve connection timeout problems.
    n = 0
    while n <= 3:
        try:
            r = requests.post(url=url, data=payload, headers=headers, timeout=60)
            break
        except Exception, e:
            print(e)
            n += 1
    if 'ErrorInfo' in r.json():
        errors = r.json()['ErrorInfo']
        # stop requests when encountered ip constraints.
        if re.search(r'IP', errors) and re.search(r'VIP', errors):
            raise Exception('ENCOUNTERED IP CONSTRAINTS.')
        logging.warn('ERRORS: {stknm}_{year} encounter {error}.'\
                     .format(stknm=stknm,
                             year=year,
                             error=errors.encode('utf-8')
                             )
                     )
    else:
        dump_data(json_dct=r.json(), stknm=stknm, year=year)
    time.sleep(1)


def main():
    with open(target_stknms_txt, 'r') as f:
        target_stknms_lst = f.read().split(',')
    with open(crawled_stknms_txt, 'r') as f:
        crawled_stknms_lst = f.read().split('\n')
        crawled_stknms_lst = [stknm.strip() for stknm in crawled_stknms_lst]
    years = range(2014, 2017)
    for stknm in target_stknms_lst:
        for year in years:
            if '{year}_{stknm}.pickle'.format(year=year, stknm=stknm) in crawled_stknms_lst:
                print('{year}_{stknm}.pickle.'.format(year=year, stknm=stknm))
                continue
            crawl_by_stknm_year(stknm=stknm, year=year)
        commands.getstatusoutput("echo '{stknm}' >> {fname}".\
                                 format(stknm=stknm, fname=crawled_stknms_txt))


if __name__ == '__main__':
    main()
