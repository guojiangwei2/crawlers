#!/usr/bin/env python
# -*- coding: utf-8 -*-

target_stknms_txt = 'target_stknms.txt'
crawled_stknms_txt = 'crawled_stknms.txt'

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
    'Cookie': ('JSESSIONID=vb87dm46litr1at8rltyl0l5h; Hm_lvt_9ebd156ac7d2304301a6a7f0434e8257=1488609334; '
               'Hm_lpvt_9ebd156ac7d2304301a6a7f0434e8257=1488685121'),
    'Host': 'www.innojoy.com',
    'Origin': 'http://www.innojoy.com',
    'Referer': 'http://www.innojoy.com/searchresult/default.html',
    'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/56.0.2924.87 Safari/537.36'),
    'X-Requested-With': 'XMLHttpRequest'
}
