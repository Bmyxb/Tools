# Tools
Handy scripts and useful tools

## 1. clear_data.py (py3)
A simple script for deleting keys with no expire time or start with certain prefix.
> pip3 install redis

- clear data with no expire
> python3 clear_data.py 127.0.0.1 6379 [password] clear_no_expire

- clear data start with [prefix]
> python3 clear_data.py 127.0.0.1 6379 [password] clear_prefix [prefix]

## 2. stat_key_size.py (py3)
This script is used to detect big keys for analyzing memory usage.(Using rdb is also an option).
'stat_lower_bound' filters small keys size < lower bound.
'log_item' 1 means output eahc item in a list(large than lower bound) too, ignore or 0 to close.
> python3 stat_key_size.py 127.0.0.1 6379 [password] [stat_lower_bound] *[log_item]