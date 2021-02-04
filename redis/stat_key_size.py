#!/bin/python
# -*- coding:utf-8 -*-

import sys
import redis
import logging
from datetime import datetime

# logging style
def initLogSetting():
    date = datetime.now().strftime('%y%m%d_%H_%M')
    filename = '.log/stat_' + date + '.log'
    logging.basicConfig(
        level = logging.INFO,
        format = '%(asctime)s  %(filename)s : %(levelname)s  %(message)s',
        datefmt = '%Y-%m-%d %A %H:%M:%S',
        filename = filename,
        filemode = 'w'
    )

def count_list(l, log_item):
    list_len = 0
    for l_item in l:
        item_len = len(l_item)
        list_len += item_len
        if log_item and item_len > stat_size:
            log_line = "item | key:%s len:%d" % (l_item, item_len)
            logging.info(log_line)
    return list_len

# stat size for all keys
def stat_key_size(host, port, password, stat_size, log_item):
    initLogSetting()
    r = redis.StrictRedis(host=host, port=port, password=password, socket_connect_timeout=10)
    n = 0
    total_cnt = r.dbsize()
    total_len = 0
    while True:
        n, key_list = r.scan(cursor=n, count=5000)
        for key in key_list:
            try:
                key = key.decode()
                t = r.type(key).decode()
                if  t == 'string':
                    v = r.get(key)
                    item_len = len(v)
                    total_len += item_len
                    if item_len > stat_size:
                        log_line = "key: %s | len:%d " % (key, item_len)
                        logging.info(log_line)
                elif t == 'list':
                    l = r.lrange(key, 0, -1)
                    list_len = count_list(l)
                    total_len += list_len
                    if list_len > stat_size:
                        logging.info("list key:%s len:%d" % (key, list_len))
                elif t == 'set':
                    l = r.smembers(key)
                    list_len = count_list(l, log_item)
                    total_len += list_len
                    if list_len > stat_size:
                        logging.info("set key:%s len:%d" % (key, list_len))
                elif t == 'sorted set':
                    l = r.zrange(key, 0, -1)
                    list_len = count_list(l, log_item)
                    total_len += list_len
                    if list_len > stat_size:
                        logging.info("sorted set key:%s len:%d" % (key, list_len))
                elif t == 'hash':
                    l = r.hgetall(key, 0, -1)
                    list_len = count_list(l, log_item)
                    total_len += list_len
                    if list_len > stat_size:
                        logging.info("hash key:%s len:%d" % (key, list_len))
            # in case key deleted
            except TypeError:
                continue
        # no more data                
        if n == 0:
            break
    print("Total : %s"  % total_cnt)
    print("Total len: %s" % total_len)

def print_instruct():
    print('Usage: python', sys.argv[0], 'host port password stat_size [log_item]')
    print('  stat_size - the lower bound for a key to be logged')
    print('  log_item - add logging for size of each item in lists and sets')

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print_instruct()
        exit(1)
    db_host = sys.argv[1]
    db_port = sys.argv[2]
    db_password = sys.argv[3]
    stat_size = int(sys.argv[4])
    log_item = len(sys.argv) == 6
    
    stat_key_size(db_host, db_port, db_password, stat_size, log_item)
    
