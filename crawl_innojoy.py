# -*- coding: utf-8 -*-

import re
import json
import time
import numpy as np
import pandas as pd
import cPickle
import requests
import logging
from consts import innojoy_url, payload, get_headers, get_proxies, candi_csv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)


def compose_payload(stknm, year):
    query_str = '\'{stknm}\' and ADY={year}'.format(stknm=stknm.encode('utf-8'), year=year)
    payload['patentSearchConfig'].update({'Query': query_str})
    return json.dumps(payload)


def dump_data(json_dct, stknm, year):
    cPickle.dump(json_dct, open('data/{year}_{stknm}.pickle'.format(year=year, stknm=stknm.encode('utf-8')), 'w'))


def main():
    df_data = pd.read_csv(candi_csv, dtype={'year': str, 'name': str}, encoding='utf-8')

    proxies_lst = []
    for _, row in df_data.iterrows():
        stknm = row['name']
        year = row['year']
        is_crawled = row['is_crawled']

        # 已经处理过的数据直接跳过
        if is_crawled:
            logger.info('Stock {stknm} has been crawled.'.format(stknm=stknm.encode('utf-8')))
            continue

        logger.info("Start crawl {stknm}...".format(stknm=stknm.encode('utf-8')))
        _payload = compose_payload(stknm=stknm, year=year)

        # 请求目标网址3次
        n = 3
        while n:
            # query proxies if there's not available in list
            if not proxies_lst:
                time.sleep(3)
                proxies_lst = get_proxies()
                if not proxies_lst:
                    logger.warning("Proxies does not work.")
                    raise Exception('Proxies does not work.')
            proxies = proxies_lst.pop()

            try:
                resp = requests.post(
                    url=innojoy_url,
                    data=_payload,
                    headers=get_headers(),
                    proxies=proxies,
                    timeout=10
                )
                # properly get data and raise no error, break this loop
                if not re.search(r'error', resp.content, re.IGNORECASE):
                    logger.info("Crawl stock {stknm} done.".format(stknm=stknm.encode('utf-8')))
                    break
            except Exception as e:
                print(repr(e))
            logger.info("Crawl stock {stknm} {cnt} times...".format(stknm=stknm.encode('utf-8'), cnt=4 - n))
            n -= 1
            time.sleep(1)

        # 保存爬取的数据
        if 'ErrorInfo' in resp.json():
            errors = resp.json()['ErrorInfo']
            # IP限制的时候，暂停程序
            if re.search(r'IP', errors) and re.search(r'VIP', errors):
                raise Exception('ENCOUNTERED IP CONSTRAINTS.')
            logging.warn('ERRORS: {stknm}_{year} encounter {error}.'.format(stknm=stknm.encode('utf-8'), year=year,
                                                                            error=errors.encode('utf-8')))
        else:
            dump_data(json_dct=resp.json(), stknm=stknm, year=year)
            logger.info("Dump stock {stknm} done.".format(stknm=stknm.encode('utf-8')))

        # 修改目标csv的字段，将是否处理字段置为1并保存
        df_data.loc[np.logical_and(df_data.name == stknm, df_data.year == year), 'is_crawled'] = 1
        df_data.to_csv(candi_csv, encoding='utf-8', index=False)


if __name__ == '__main__':
    main()
