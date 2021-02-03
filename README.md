# Tools
Handy scripts and useful tools

## 1. clear_data.py (py3)
A simple script for deleting keys with no expire time or start with certain prefix.
> pip3 install redis

- clear data with no expire
> python clear_data.py 127.0.0.1 6379 [password] clear_no_expire

- clear data start with [prefix]
> python clear_data.py 127.0.0.1 6379 [password] clear_prefix [prefix]