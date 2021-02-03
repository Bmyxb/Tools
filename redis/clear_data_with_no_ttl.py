#!/bin/python
# -*- coding:utf-8 -*-

import sys
import redis
import logging
from datetime import datetime

# define logging style for removed keys
def initLogSetting():
    date = datetime.now().strftime('_%y%m%d_%H_%M')
    filename = './clear_' + date + '.log'
    logging.basicConfig(
        level = logging.INFO,
        format = '%(asctime)s  %(filename)s : %(levelname)s  %(message)s',
        datefmt = '%Y-%m-%d %A %H:%M:%S',
        filename = filename,
        filemode = 'w'
    )

# clear keys with no expire time
def clear_no_expire(host, port, password):
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

def print_instruct():
    print('Usage: python ', sys.argv[0], ' host port password op [prefix]')
    print('op: ')
    print(' clear_no_expire - clear all data with no expire time')
    print(' clear_prefix - clear data starts with [prefix]')

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print_instruct()
        exit(1)
    db_host = sys.argv[1]
    db_port = sys.argv[2]
    db_password = sys.argv[3]
    op = sys.argv[4]
    if op == 'clear_no_expire':
        clear_no_expire(db_host, db_port, db_password)
    elif op == 'clear_prefix':
        if len(sys.argv) != 6:
            print_instruct()
            exit(1)
        prefix = sys.argv[6]
        clear_data_with_prefix(db_host, db_port, db_password, prefix)

