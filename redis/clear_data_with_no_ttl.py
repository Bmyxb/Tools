#!/bin/python
# -*- coding:utf-8 -*-

import redis
import logging
from datetime import datetime

# define logging style for removed keys
def initLogSetting():
    date = datetime.now().strftime('%y%m%d')
    filename = './clear_' + date + '.log'
    logging.basicConfig(
        level = logging.INFO,
        format = '%(asctime)s  %(filename)s : %(levelname)s  %(message)s',
        datefmt = '%Y-%m-%d %A %H:%M:%S',
        filename = filename,
        filemode = 'w'
    )

# clear keys with no ttl
def clear_no_ttl(host, port, password):
    initLogSetting()
    r = redis.StrictRedis(host=host, port=port, password=password, socket_connect_timeout=10)
    n = 0
    remove_cnt = 0
    total_cnt = r.dbsize()
    while True:
        n, key_list = r.scan(cursor=n, count=5000)
        for key in key_list:
            if r.ttl(key) == -1:
                r.delete(key)
                remove_cnt += 1
                logging.info("Del key: %s " % key)
        # no more data                
        if n == 0:
            break
    print("Total : %s"  % total_cnt)
    print("Removed : %s" % remove_cnt)

# clear keys with prefix
def clear_data_with_prefix(host, port, password, prefix):
    initLogSetting()
    r = redis.StrictRedis(host=host, port=port, password=password, socket_connect_timeout=10)
    n = 0
    remove_cnt = 0
    total_cnt = r.dbsize()
    while True:
        n, key_list = r.scan(cursor=n, count=5000)
        for key in key_list:
            if str(key).startswith(prefix):
                r.delete(key)
                remove_cnt += 1
                logging.info("Del key: %s " % key)
        # no more data                
        if n == 0:
            break
    print("Total : %s"  % total_cnt)
    print("Removed : %s" % remove_cnt)


if __name__ == '__main__':
    # 获取redis数据
    host = '127.0.0.1'
    port = 6379
    password = ''
    clear_no_ttl(host, port, password)
    clear_data_with_prefix(host, port, password, "push")
    
